#!/usr/bin/env python3

import logging
import os
import sys

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


def process_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()
        text = convert_html_to_text(html_content)
        if text:
            with open(filepath.replace('.html', '.txt'), 'w', encoding='utf-8') as file:
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


def convert_files_in_directory(directory):
    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue
        if filename.endswith('.html'):
            process_html_file(os.path.join(directory, filename))
        elif filename.endswith('.pdf'):
            process_pdf_file(os.path.join(directory, filename))


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


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_files.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"The specified directory {directory} does not exist.")
        sys.exit(1)

    convert_files_in_directory(directory)
    concatenate_text_files(directory)


if __name__ == "__main__":
    main()
