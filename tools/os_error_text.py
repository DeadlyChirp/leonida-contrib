"""One-line text for an OSError that shows its path the way the user wrote it.

str(OSError) quotes the path with repr(), so on Windows every backslash comes out doubled:
"[Errno 13] Permission denied: 'C:\\\\Users\\\\me\\\\blocked'". os_error_text() keeps the same parts (the
[Errno N] or [WinError N] code, the message, and both paths of a rename) but prints each path as written.
"""
from __future__ import annotations

import os


def _path_text(path) -> str:
    if isinstance(path, (str, bytes, os.PathLike)):
        return os.fsdecode(path)
    return str(path)


def os_error_text(error: BaseException) -> str:
    """str(error), except that an OSError's paths are printed as written instead of as repr()."""
    if not isinstance(error, OSError) or error.filename is None or not error.strerror:
        return str(error)
    winerror = getattr(error, "winerror", None)
    if winerror is not None:
        code = f"[WinError {winerror}] "
    elif error.errno is not None:
        code = f"[Errno {error.errno}] "
    else:
        code = ""
    text = f"{code}{error.strerror}: {_path_text(error.filename)}"
    if error.filename2 is not None:
        text += f" -> {_path_text(error.filename2)}"
    return text
