import os
import tempfile
from pathlib import Path

from cpp_guard_analyzer.analyzer import analyze_file, suggest_macro


def write_header(tmpdir, name, content):
    path = Path(tmpdir) / name
    path.write_text(content)
    return path


def test_missing_guard(tmp_path):
    path = write_header(tmp_path, "a.h", "// no guard\nint x;\n")
    analysis = analyze_file(path, Path(tmp_path))
    assert analysis["guard_type"] is None
    assert "Missing #endif" in analysis["messages"]


def test_pragma_once(tmp_path):
    path = write_header(tmp_path, "b.hpp", "#pragma once\nint y;\n")
    analysis = analyze_file(path, Path(tmp_path))
    assert analysis["guard_type"] == "pragma"


def test_macro_guard(tmp_path):
    path = write_header(tmp_path, "c.h", "#ifndef C_H\n#define C_H\nint z;\n#endif // C_H\n")
    analysis = analyze_file(path, Path(tmp_path))
    assert analysis["guard_type"] == "macro"
    assert analysis["macro"] == "C_H"
    assert analysis["suggested_macro"] == "C_H"


def test_suggest_macro(tmp_path):
    path = write_header(tmp_path, "subdir/d.h", "#ifndef SUBDIR_D_H\n#define SUBDIR_D_H\nint d;\n#endif\n")
    macro = suggest_macro(path, Path(tmp_path))
    assert macro == "SUBDIR_D_H"
