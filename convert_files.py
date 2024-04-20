#!/usr/bin/env python3

import glob
import logging
import os
import sys

import epub
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def convert_html_to_text(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        logging.error(f"Error converting HTML to text: {e}")
        return None


def convert_pdf_to_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
    except Exception as e:
        logging.error(f"Error converting PDF to text: {e}")
        return None


def convert_epub_to_text(epub_path):
    try:
        book = epub.open_epub(epub_path)
        text = ''
        for item_id, item in book.opf.manifest.items():
            # Ensure the type is text and the format is HTML (common in EPUB)
            if item.media_type == 'application/xhtml+xml':
                content = book.read_item(item)
                soup = BeautifulSoup(content, 'html.parser')
                text += soup.get_text() + '\n'
        book.close()
        return text
    except Exception as e:
        logging.error(f"Error converting EPUB to text: {e}")
        return None


def process_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
        text = convert_html_to_text(html_content)
        if text:
            txt_filepath = filepath.rsplit('.', 1)[0] + '.txt'  # This handles both .html and .htm extensions
            with open(txt_filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            logging.info(f"Converted {os.path.basename(filepath)} to text")
    except Exception as e:
        logging.error(f"Error processing {os.path.basename(filepath)}: {e}")


def process_pdf_file(filepath):
    text = convert_pdf_to_text(filepath)
    if text:
        with open(filepath.replace('.pdf', '.txt'), 'w', encoding='utf-8') as file:
            file.write(text)
        logging.info(f"Converted {os.path.basename(filepath)} to text")


def process_epub_file(filepath):
    # text = convert_epub_to_text(filepath)
    text = convert_epub_to_text(filepath)
    if text:
        with open(filepath.replace('.epub', '.txt'), 'w', encoding='utf-8') as file:
            file.write(text)
        logging.info(f"Converted {os.path.basename(filepath)} to text")


def concatenate_text_files(directory):
    directory_name = os.path.basename(os.path.normpath(directory))
    output_file = os.path.join(directory, directory_name + "_concatenated.txt")

    text_files = [f for f in os.listdir(directory) if f.endswith('.txt') and os.path.isfile(os.path.join(directory, f))]
    text_files.sort()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in text_files:
            if filename == os.path.basename(output_file):
                continue
            outfile.write(f"----- Start of {filename} -----\n")
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)
                outfile.write("\n\n")
            outfile.write(f"----- End of {filename} -----\n\n")


def process_file(filepath):
    if filepath.endswith('.html') or filepath.endswith('.htm'):
        process_html_file(filepath)
    elif filepath.endswith('.pdf'):
        process_pdf_file(filepath)
    elif filepath.endswith('.epub'):
        process_epub_file(filepath)
    else:
        logging.error(f"Unsupported file type: {filepath}")


def process_directory(directory):
    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue
        process_file(os.path.join(directory, filename))
    concatenate_text_files(directory)


def process_files_with_wildcard(pattern):
    for filepath in glob.glob(pattern):
        if os.path.isfile(filepath):
            process_file(filepath)
        else:
            logging.warning(f"Skipping non-file: {filepath}")


def display_help():
    help_message = """
    Usage: python convert_files.py <path or pattern>

    This script converts HTML and PDF files to text files. It automatically detects 
    whether the input is a directory, a single file, or multiple files using a wildcard pattern.

    - If a directory is specified, all HTML and PDF files within that directory are processed.
    - If a single file is specified, only that file is processed.
    - If a pattern is specified (e.g., '*.pdf'), all matching files are processed.

    Examples:
        python convert_files.py /path/to/directory
        python convert_files.py /path/to/file.pdf
        python convert_files.py "*.html"

    The script supports '.html', '.htm', and '.pdf' files. For HTML and PDF files, 
    it generates corresponding text files. When processing directories or patterns,
    it also creates a concatenated text file of all processed files.

    Use the -h or --help flag for displaying this help message.
    """
    print(help_message)


def process_files(pattern):
    matched_files = glob.glob(pattern)
    if not matched_files:
        logging.error(f"No files found for the pattern: {pattern}")
        return

    for filepath in matched_files:
        if os.path.isfile(filepath):
            process_file(filepath)
        else:
            logging.warning(f"Skipping non-file: {filepath}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        display_help()
        sys.exit(0)

    path_or_pattern = sys.argv[1]

    if os.path.isdir(path_or_pattern):
        process_directory(path_or_pattern)
    elif os.path.isfile(path_or_pattern):
        process_file(path_or_pattern)
    else:
        process_files(path_or_pattern)


if __name__ == "__main__":
    main()
