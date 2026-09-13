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
    return Path(__file__).resolve().parents[2]


def _resolve_git_dir(root: Path) -> Path | None:
    """Return the repository's git directory, including worktree-style .git files."""
    git_path = root / ".git"
    if git_path.is_dir():
        return git_path
    if git_path.is_file():
        try:
            text = git_path.read_text(encoding="utf-8").strip()
            if text.lower().startswith("gitdir:"):
                target = text.split(":", 1)[1].strip()
                path = Path(target)
                if not path.is_absolute():
                    path = (root / path).resolve()
                return path
        except OSError:
            pass
    return None


def _git_commit_from_files(root: Path) -> str | None:
    """Read HEAD directly so GitHub Desktop clones work even without git.exe in PATH."""
    git_dir = _resolve_git_dir(root)
    if git_dir is None:
        return None

    try:
        head = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
    except OSError:
        return None

    if not head.startswith("ref: "):
        return head or None

    ref = head[5:].strip()
    ref_file = git_dir / ref
    try:
        if ref_file.is_file():
            return ref_file.read_text(encoding="utf-8").strip() or None
    except OSError:
        pass

    packed_refs = git_dir / "packed-refs"
    try:
        if packed_refs.is_file():
            for line in packed_refs.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("^"):
                    continue
                parts = line.split(" ", 1)
                if len(parts) == 2 and parts[1] == ref:
                    return parts[0]
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
