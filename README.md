# cpp-guard-analyzer

A lightweight offline CLI that scans C++ header files for include guards, reports inconsistencies, detects duplicate guard names, and can optionally insert missing guards or replace mismatched guard names.

## Features

* Detects traditional `#ifndef / #define / #endif` guards.
* Detects `#pragma once`.
* Checks that guard macros follow a simple convention based on the file path.
* Detects duplicate guard names across the codebase.
* Reports missing `#endif` comments.
* Optional `--fix` flag to insert missing guards or replace mismatched guard names.

## Installation

```bash
pip install git+https://github.com/ScobieWorks/cpp-guard-analyzer.git
```

## Usage

```bash
cpp-guard-analyzer <root_dir> [--fix]
```

* `<root_dir>` – Directory to scan.
* `--fix` – Apply automatic fixes to header files.

## Example

```bash
cpp-guard-analyzer src
```

The tool will print a concise report to stdout.

## License

MIT License – see the LICENSE file.


## Support

If this project saved you time, optional support is welcome: https://paypal.me/Damonwill
