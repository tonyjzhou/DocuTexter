
# File Converter Script

This Python script automates the conversion of HTML and PDF files to text files so that it can be easily processed by ChatGPT and other LLM systems. 

It supports processing individual files, all files in a directory, or files matching a wildcard pattern.

## Features

- Automatically detects whether the input is a directory, a single file, or multiple files using a wildcard pattern.
- Converts HTML and PDF files to text files.
- Concatenates all converted text files into a single file when processing directories or patterns.

## Usage

```bash
python convert_files.py <path or pattern>
```

- If a directory is specified, all HTML and PDF files within that directory are processed.
- If a single file is specified, only that file is processed.
- If a pattern is specified (e.g., '*.pdf'), all matching files are processed.

## Examples

```bash
python convert_files.py /path/to/directory
python convert_files.py /path/to/file.pdf
python convert_files.py "*.html"
```

## Requirements

- Python 3
- BeautifulSoup
- PyPDF2

## Installation

Make sure Python 3 is installed on your system. If not, you can download it from [Python's official website](https://www.python.org/downloads/).

To install the required packages, run:

```bash
pip install beautifulsoup4 PyPDF2
```

## Help

Use the `-h` or `--help` flag to display the help message:

```bash
python convert_files.py -h
```

---

For more information, please refer to the script's comments.
