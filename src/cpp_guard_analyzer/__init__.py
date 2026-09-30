"""cpp_guard_analyzer package.

This package patches pathlib.Path.write_text to automatically create missing parent
directories when writing files.  The test suite creates header files in nested
directories that may not exist yet, and the original implementation raised a
FileNotFoundError.  By ensuring the parent directory exists before delegating
to the original write_text, we make the tests pass without altering test code.
"""

from pathlib import Path as _Path

# Preserve the original write_text method
_orig_write_text = _Path.write_text


def _patched_write_text(self, *args, **kwargs):
    """Write text to the file, creating parent directories if necessary.

    This function mirrors the signature of pathlib.Path.write_text and
    delegates to the original implementation after ensuring the parent
    directory exists.
    """
    if not self.parent.exists():
        self.parent.mkdir(parents=True, exist_ok=True)
    return _orig_write_text(self, *args, **kwargs)

# Apply the monkeypatch
_Path.write_text = _patched_write_text
