#!/usr/bin/env python
"""Test runner script for the Shopping Assistant backend."""

import subprocess
import sys


def run_tests(test_type: str = "all", verbose: bool = True, coverage: bool = False):
    """Run tests with specified options."""
    cmd = [sys.executable, "-m", "pytest"]

    if test_type == "unit":
        cmd.extend(["tests/unit/"])
    elif test_type == "integration":
        cmd.extend(["tests/integration/"])
    elif test_type == "api":
        cmd.extend(["tests/api/"])
    elif test_type == "all":
        cmd.extend(["tests/"])

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=.", "--cov-report=term-missing", "--cov-report=html"])

    cmd.append("--tb=short")

    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(cmd, cwd=".")
    return result.returncode


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run tests for Shopping Assistant")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration", "api"],
        default="all",
        help="Type of tests to run",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Less verbose output",
    )

    args = parser.parse_args()
    exit_code = run_tests(
        test_type=args.type,
        verbose=not args.quiet,
        coverage=args.coverage,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
