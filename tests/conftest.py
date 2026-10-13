"""Windows compatibility shim for gltest Direct Mode.

gltest replaces fd 0 with a temporary file and immediately unlinks that file.
POSIX permits that sequence, while Windows keeps the file locked until fd 0 is
restored.  Delay only that unlink until interpreter shutdown; no VM behavior is
changed.
"""
import atexit
import os

from gltest.direct import loader


_original_inject = loader._inject_message_to_fd0
_deferred_paths: list[str] = []


def _windows_safe_inject(vm):
    original_unlink = os.unlink

    def defer_unlink(path):
        _deferred_paths.append(path)

    os.unlink = defer_unlink
    try:
        _original_inject(vm)
    finally:
        os.unlink = original_unlink


def _cleanup_deferred_files():
    for path in _deferred_paths:
        try:
            os.unlink(path)
        except OSError:
            pass


if os.name == "nt":
    loader._inject_message_to_fd0 = _windows_safe_inject
    atexit.register(_cleanup_deferred_files)
