import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Regular expressions for include guard detection
_PRAGMA_RE = re.compile(r"^\s*#\s*pragma\s+once", re.IGNORECASE)
_IFNDEF_RE = re.compile(r"^\s*#\s*ifndef\s+(\w+)")
_DEFINE_RE = re.compile(r"^\s*#\s*define\s+(\w+)")
_ENDIF_RE = re.compile(r"^\s*#\s*endif")

# A simple guard naming convention: UPPERCASE relative path with slashes and dots replaced by underscores, ending with _H

def suggest_macro(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = rel.parts
    macro = "_".join(part.upper() for part in parts)
    macro = macro.replace(".", "_")
    return f"{macro}_H"


def analyze_file(file_path: Path, root: Path) -> Dict:
    """Return analysis dict for a single header file."""
    data = {
        "path": str(file_path),
        "guard_type": None,  # 'pragma', 'macro', or None
        "macro": None,
        "suggested_macro": None,
        "duplicate": False,
        "missing_endif_comment": False,
        "messages": [],
    }
    lines = file_path.read_text(encoding="utf-8").splitlines()
    # Detect pragma once
    for i, line in enumerate(lines):
        if _PRAGMA_RE.match(line):
            data["guard_type"] = "pragma"
            break
    if data["guard_type"] is None:
        # Look for macro guard
        guard_start = None
        guard_macro = None
        for i, line in enumerate(lines):
            m = _IFNDEF_RE.match(line)
            if m:
                guard_start = i
                guard_macro = m.group(1)
                break
        if guard_start is not None:
            # Verify following #define
            for j in range(guard_start + 1, len(lines)):
                m = _DEFINE_RE.match(lines[j])
                if m:
                    if m.group(1) == guard_macro:
                        data["guard_type"] = "macro"
                        data["macro"] = guard_macro
                        break
                    else:
                        data["messages"].append("#define macro does not match #ifndef")
                        break
            if data["guard_type"] is None:
                data["messages"].append("Missing matching #define for #ifndef")
    if data["guard_type"] == "macro":
        data["suggested_macro"] = suggest_macro(file_path, root)
        if data["macro"] != data["suggested_macro"]:
            data["messages"].append("Guard macro does not follow convention")
    # Check for #endif
    endif_found = any(_ENDIF_RE.match(l) for l in lines)
    if not endif_found:
        data["messages"].append("Missing #endif")
    else:
        # Check if last #endif has comment matching macro
        for l in reversed(lines):
            if _ENDIF_RE.match(l):
                if data["guard_type"] == "macro":
                    if f"{data['macro']}" not in l:
                        data["missing_endif_comment"] = True
                break
    return data


def find_headers(root: Path) -> List[Path]:
    return list(root.rglob("*.h")) + list(root.rglob("*.hpp"))


def analyze_directory(root: Path) -> Tuple[List[Dict], Dict[str, List[str]]]:
    """Return list of analyses and a dict mapping guard macros to file paths."""
    analyses = []
    guard_map: Dict[str, List[str]] = {}
    for header in find_headers(root):
        analysis = analyze_file(header, root)
        analyses.append(analysis)
        if analysis["guard_type"] == "macro" and analysis["macro"]:
            guard_map.setdefault(analysis["macro"], []).append(analysis["path"])
    # Mark duplicates
    for macro, paths in guard_map.items():
        if len(paths) > 1:
            for path in paths:
                for a in analyses:
                    if a["path"] == path:
                        a["duplicate"] = True
                        a["messages"].append(f"Duplicate guard macro: {macro}")
    return analyses, guard_map


def fix_file(file_path: Path, root: Path, analysis: Dict) -> None:
    """Apply fixes to a single file based on analysis."""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if analysis["guard_type"] == "pragma":
        # Replace pragma once with macro guard
        macro = analysis["suggested_macro"]
        new_lines = [f"#ifndef {macro}", f"#define {macro}"] + lines + [f"#endif // {macro}"]
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    elif analysis["guard_type"] == "macro":
        macro = analysis["macro"]
        suggested = analysis["suggested_macro"]
        if macro != suggested:
            # Replace macro names
            new_lines = []
            for l in lines:
                if _IFNDEF_RE.match(l) or _DEFINE_RE.match(l):
                    new_lines.append(re.sub(r"\b" + re.escape(macro) + r"\b", suggested, l))
                else:
                    new_lines.append(l)
            # Ensure #endif comment
            for i in range(len(new_lines)-1, -1, -1):
                if _ENDIF_RE.match(new_lines[i]):
                    if f"{suggested}" not in new_lines[i]:
                        new_lines[i] = f"#endif // {suggested}"
                    break
            file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    else:
        # No guard – insert one
        macro = analysis["suggested_macro"]
        new_lines = [f"#ifndef {macro}", f"#define {macro}"] + lines + [f"#endif // {macro}"]
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
