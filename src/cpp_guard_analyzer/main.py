import argparse
import sys
from pathlib import Path

from .analyzer import analyze_directory, fix_file


def print_report(analyses):
    for a in analyses:
        status = []
        if a["guard_type"] is None:
            status.append("MISSING GUARD")
        elif a["guard_type"] == "pragma":
            status.append("PRAGMA ONCE")
        else:
            status.append("GUARD")
        if a["duplicate"]:
            status.append("DUPLICATE")
        if a["missing_endif_comment"]:
            status.append("MISSING ENDIF COMMENT")
        if a["messages"]:
            status.append("; ".join(a["messages"]))
        print(f"{a['path']}: {', '.join(status)}")


def main():
    parser = argparse.ArgumentParser(description="C++ header include guard analyzer")
    parser.add_argument("root", type=Path, help="Root directory to scan")
    parser.add_argument("--fix", action="store_true", help="Apply automatic fixes")
    args = parser.parse_args()

    if not args.root.is_dir():
        print("Error: root must be a directory", file=sys.stderr)
        sys.exit(1)

    analyses, _ = analyze_directory(args.root)
    if args.fix:
        for a in analyses:
            fix_file(Path(a["path"]), args.root, a)
    print_report(analyses)


if __name__ == "__main__":
    main()
