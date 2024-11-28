# Web Archiver

**Web Archiver** is a simple tool for downloading and backing up an entire website's contents, including HTML pages, CSS, JavaScript, images, and PHP files.

## Features

- Downloads the main HTML page and saves it locally.
- Creates directories for CSS, JavaScript, images, and PHP files.
- Supports multiple operating systems (Windows, Linux, macOS).
- Simple command-line interface for easy use.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

To install the required libraries, run the following command:

```
pip install requests 
```
```
pip install beautifulsoup4
```
Usage

1. Clone the repository:
```
git clone https://github.com/archescyber/web-archiver.git
```
```
cd web-archiver
```


2. Run the script:
```
python main.py
```

3. Enter the website address you want to back up (e.g., https://example.com).


4. The files will be saved in a directory named example-com-site-backup in your current working directory.

