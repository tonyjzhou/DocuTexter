#!/usr/bin/env python3

import logging
import os
import sys

from PyPDF2 import PdfReader
from bs4 import BeautifulSoup


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
            num_pages = len(reader.pages)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        logging.error(f"Error converting PDF to text: {e}")
        return None


def convert_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.html'):
            try:
                with open(filepath, 'r') as file:
                    html_content = file.read()
                text = convert_html_to_text(html_content)
                if text:
                    with open(filepath.replace('.html', '.txt'), 'w') as file:
                        file.write(text)
                    logging.info(f"Converted {filename} to text")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
        elif filename.endswith('.pdf'):
            text = convert_pdf_to_text(filepath)
            if text:
                with open(filepath.replace('.pdf', '.txt'), 'w') as file:
                    file.write(text)
                logging.info(f"Converted {filename} to text")


def concatenate_text_files(directory):
    # Extract the directory name to use as the output file name
    directory_name = os.path.basename(os.path.normpath(directory))
    output_file = os.path.join(directory, directory_name + "_concatenated.txt")

    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    text_files.sort()  # Sorting the files by name

    with open(output_file, 'w') as outfile:
        for filename in text_files:
            if filename == os.path.basename(output_file):
                continue  # Skip the output file itself if it's in the same directory
            outfile.write(f"----- Start of {filename} -----\n")
            with open(os.path.join(directory, filename), 'r') as infile:
                outfile.write(infile.read())
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

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    convert_files_in_directory(directory)
    concatenate_text_files(directory)


if __name__ == "__main__":
    main()
