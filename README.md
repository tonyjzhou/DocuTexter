# DocuTexter

## Overview
DocuTexter is a Python tool designed to convert HTML and PDF files into plain text format. It can process individual files or an entire directory, converting each file and then concatenating the results into a single text file.

## Dependencies
- BeautifulSoup4: For parsing HTML content.
- PyPDF2: For reading and extracting text from PDF files.

## Setup
1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use DocuTexter, run the script from the command line with a directory path as an argument. The script will process all HTML and PDF files within the specified directory.

```
python convert_files.py <directory>
```

The script will create a `.txt` file for each HTML and PDF file in the directory. After processing all files, it will generate a concatenated text file containing the content of all individual text files.

## License
This project is open-source and available under [MIT License](https://opensource.org/licenses/MIT).