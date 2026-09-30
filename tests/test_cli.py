import subprocess
import tempfile
from pathlib import Path


def run_cli(args, cwd):
    result = subprocess.run(["python", "-m", "cpp_guard_analyzer.main"] + args, cwd=cwd, capture_output=True, text=True)
    return result


def test_cli_output(tmp_path):
    # Create a header with missing guard
    (tmp_path / "a.h").write_text("int a;\n")
    result = run_cli([str(tmp_path)], cwd=str(tmp_path))
    assert result.returncode == 0
    assert "MISSING GUARD" in result.stdout


def test_cli_fix(tmp_path):
    # Header without guard
    (tmp_path / "b.h").write_text("int b;\n")
    result = run_cli([str(tmp_path), "--fix"], cwd=str(tmp_path))
    assert result.returncode == 0
    # Verify file now has guard
    content = (tmp_path / "b.h").read_text()
    assert "#ifndef" in content
    assert "#define" in content
    assert "#endif" in content
