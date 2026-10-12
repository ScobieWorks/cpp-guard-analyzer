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

<!-- ORION_MONETIZATION_PILOT_START -->

## C++ Header Guard Audit Pilot

For a limited 7-day pilot, ScobieWorks offers a **C++ Header Guard Audit for
$149 USD**. This price is an experiment hypothesis, not market evidence.

### Proposed paid scope

- One public C/C++ repository and one bounded include-guard analysis pass
- Review of missing, inconsistent, or problematic header guards
- Prioritized findings and suggested corrections/refactoring
- Optional generated patch recommendations
- A concise written report, with a maximum of two operator hours

The free cpp-guard-analyzer tool remains fully available; no capability is removed.
There is no promise of automated source modification of your repository.
No private repository access or credentials are requested. No payment automation.

Interested in the paid pilot? Open a GitHub issue in this repository titled exactly:

**C++ Header Guard Audit Pilot**

An issue is only a possible lead, not a purchase or evidence of willingness to pay.
Do not include credentials, secrets, or private source code.

<!-- ORION_MONETIZATION_PILOT_END -->
