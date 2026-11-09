import sys
import json
import argparse
from pathlib import Path
from typing import Optional, NoReturn

# ANSI Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def format_error(msg: str) -> str:
    return f"{RED}{BOLD}Error:{RESET} {msg}"

def validate_and_format(content: str, indent: int, sort_keys: bool) -> str:
    try:
        data = json.loads(content)
        return json.dumps(data, indent=indent, sort_keys=sort_keys)
    except json.JSONDecodeError as e:
        line_indicator = " " * (e.colno - 1) + "^"
        lines = content.splitlines()
        context = ""
        if 0 <= e.lineno - 1 < len(lines):
            context = f"\n  {lines[e.lineno-1]}\n  {YELLOW}{line_indicator}{RESET}"
        
        error_msg = f"{e.msg} at line {e.lineno}, column {e.colno}{context}"
        raise ValueError(error_msg) from e

def main() -> None:
    parser = argparse.ArgumentParser(
        description="jlint: A polished JSON validator and formatter.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("file", nargs="?", help="Path to the JSON file. Reads from stdin if omitted.")
    parser.add_argument("-i", "--indent", type=int, default=4, help="Number of spaces for indentation (default: 4).")
    parser.add_argument("-s", "--sort", action="store_true", help="Sort keys alphabetically.")
    parser.add_argument("-o", "--output", help="Write output to a file instead of stdout.")
    parser.add_argument("-c", "--check", action="store_true", help="Only check if valid, do not output formatted JSON.")

    args = parser.parse_args()

    try:
        if args.file:
            path = Path(args.file)
            if not path.exists():
                print(format_error(f"File not found: {args.file}"), file=sys.stderr)
                sys.exit(1)
            raw_content = path.read_text(encoding="utf-8")
        else:
            if sys.stdin.isatty():
                parser.print_help()
                sys.exit(0)
            raw_content = sys.stdin.read()

        if not raw_content.strip():
            print(format_error("Input is empty"), file=sys.stderr)
            sys.exit(1)

        formatted = validate_and_format(raw_content, args.indent, args.sort)

        if args.check:
            print(f"{GREEN}✓ Valid JSON{RESET}")
            sys.exit(0)

        if args.output:
            Path(args.output).write_text(formatted, encoding="utf-8")
            print(f"{GREEN}✓ Formatted JSON saved to {args.output}{RESET}")
        else:
            print(formatted)

    except ValueError as e:
        print(format_error(str(e)), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()