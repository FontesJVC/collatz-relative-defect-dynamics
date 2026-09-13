from __future__ import annotations

import io
import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text: str) -> int:
        for stream in self.streams:
            stream.write(text)
        return len(text)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def _repo_root() -> Path:
    """Best-effort repository root, independent of the shell's current directory."""
    candidates = [Path.cwd().resolve(), Path(__file__).resolve().parent]
    seen: set[Path] = set()
    for start in candidates:
        for path in (start, *start.parents):
            if path in seen:
                continue
            seen.add(path)
            if (path / ".git").exists():
                return path
    # Package layout fallback: repo/src/package/reporting.py
    return Path(__file__).resolve().parents[2]


def _resolve_git_dir(root: Path) -> Path | None:
    """Return the Git directory for normal clones and worktrees."""
    git_path = root / ".git"
    if git_path.is_dir():
        return git_path
    if git_path.is_file():
        try:
            text = git_path.read_text(encoding="utf-8", errors="replace").strip()
            if text.lower().startswith("gitdir:"):
                target = text.split(":", 1)[1].strip()
                path = Path(target)
                if not path.is_absolute():
                    path = (root / path).resolve()
                return path
        except OSError:
            pass
    return None


def _read_ref(git_dir: Path, ref: str) -> str | None:
    """Resolve a ref from loose refs, packed refs, and worktree common dirs."""
    dirs = [git_dir]

    # Worktrees can store shared refs in a common Git directory.
    commondir = git_dir / "commondir"
    try:
        if commondir.is_file():
            target = commondir.read_text(encoding="utf-8", errors="replace").strip()
            common = Path(target)
            if not common.is_absolute():
                common = (git_dir / common).resolve()
            dirs.append(common)
    except OSError:
        pass

    for base in dirs:
        ref_file = base / ref
        try:
            if ref_file.is_file():
                value = ref_file.read_text(encoding="utf-8", errors="replace").strip()
                if value:
                    return value
        except OSError:
            pass

        packed_refs = base / "packed-refs"
        try:
            if packed_refs.is_file():
                for line in packed_refs.read_text(encoding="utf-8", errors="replace").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("^"):
                        continue
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2 and parts[1] == ref:
                        return parts[0]
        except OSError:
            pass

    return None


def _git_commit_from_files(root: Path) -> str | None:
    """Read HEAD directly so GitHub Desktop clones work without git.exe in PATH."""
    git_dir = _resolve_git_dir(root)
    if git_dir is None:
        return None

    try:
        head = (git_dir / "HEAD").read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        head = ""

    if head:
        if not head.startswith("ref: "):
            return head
        ref = head[5:].strip()
        value = _read_ref(git_dir, ref)
        if value:
            return value

    # Last-resort fallback: the newest reflog entry stores the new HEAD hash.
    logs_head = git_dir / "logs" / "HEAD"
    try:
        if logs_head.is_file():
            lines = [line for line in logs_head.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
            if lines:
                fields = lines[-1].split()
                if len(fields) >= 2 and len(fields[1]) >= 7:
                    return fields[1]
    except OSError:
        pass

    return None


def _git_commit(root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        commit = completed.stdout.strip()
        if commit:
            return commit
    except Exception:
        pass

    return _git_commit_from_files(root) or "unavailable"


def run_with_report(stem: str, main_func: Callable[[], None]) -> None:
    """Run a CLI main function, mirror stdout to screen, and save a timestamped report.

    Reports are written under ``audit_results/`` at the repository root. Metadata
    records the local timestamp, command line, Python/platform information, and the
    current Git commit. The commit is read from Git metadata directly when the Git
    command-line executable is not available. Exceptions are also captured in the
    report and then re-raised.
    """
    root = _repo_root()
    results_dir = root / "audit_results"
    results_dir.mkdir(parents=True, exist_ok=True)

    started = datetime.now().astimezone()
    stamp = started.strftime("%Y%m%d_%H%M%S")
    path = results_dir / f"{stem}_{stamp}.txt"

    buffer = io.StringIO()
    original_stdout = sys.stdout
    tee = _Tee(original_stdout, buffer)
    exc_info = None

    try:
        sys.stdout = tee
        main_func()
    except BaseException:
        exc_info = sys.exc_info()
        print(f"\n[ERROR] {exc_info[1].__class__.__name__}: {exc_info[1]}")
    finally:
        sys.stdout = original_stdout

    finished = datetime.now().astimezone()
    command = " ".join([Path(sys.executable).name, *sys.argv])
    metadata = [
        "Collatz Relative Defect Dynamics - computational audit report",
        "=" * 68,
        f"report:      {stem}",
        f"started:     {started.isoformat()}",
        f"finished:    {finished.isoformat()}",
        f"elapsed_s:   {(finished - started).total_seconds():.3f}",
        f"python:      {sys.version.split()[0]}",
        f"platform:    {platform.platform()}",
        f"git_commit:  {_git_commit(root)}",
        f"repo_root:   {root}",
        f"command:     {command}",
        f"cwd:         {os.getcwd()}",
        "=" * 68,
        "",
    ]
    path.write_text("\n".join(metadata) + buffer.getvalue(), encoding="utf-8")
    print(f"\nReport saved to: {path.relative_to(root)}")

    if exc_info is not None:
        _, exc, tb = exc_info
        raise exc.with_traceback(tb)
