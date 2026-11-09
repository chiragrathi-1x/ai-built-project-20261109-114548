# jlint

`jlint` is a clean, dependency-free Python CLI tool designed to validate and pretty-print JSON files. It provides human-friendly error messages that point directly to the line and column of a syntax error.

## Features

- **Validation**: Quickly check if a file is valid JSON.
- **Formatting**: Pretty-print JSON with configurable indentation.
- **Key Sorting**: Alphabetize keys for easier diffing and reading.
- **Visual Feedback**: Precise error pointers with context lines.
- **Pipe Support**: Works with standard input/output for shell integration.
- **No Dependencies**: Uses only the Python standard library.

## Setup

Ensure you have Python 3.8+ installed.

1. **Clone or copy** the script `jlint.py` to your local machine.
2. (Optional) Install it locally to use the `jlint` command:
   ```bash
   pip install .
   ```

## Usage

### Basic Formatting
Pass a file path to print the formatted JSON to the console:
```bash
python jlint.py data.json
```

### Save to File
Use the `--output` flag to save the result:
```bash
bash python jlint.py data.json -o formatted_data.json
```

### Check Validity Only
Check if a file is valid without printing the whole content:
```bash
python jlint.py data.json --check
```

### Pipe from other commands
```bash
curl -s https://api.github.com/zen | python jlint.py
```

### Sorting Keys
```bash
python jlint.py data.json --sort
```

## Project Structure

- `jlint.py`: Main application logic.
- `test_jlint.py`: Suite of unit tests.
- `pyproject.toml`: Project configuration and CLI entry point definition.
- `.gitignore`: Standard exclusions for Python projects.

## Limitations

- **Comments**: As per the JSON standard (RFC 8259), this tool does not support comments within JSON files.
- **File Size**: Large JSON files (hundreds of MBs) may consume significant memory as the tool loads the entire structure into memory for formatting.
- **Encoding**: Primarily expects UTF-8 encoded files.

## Contributing

Contributions are welcome! Please run the tests before submitting any changes:
```bash
python test_jlint.py
```