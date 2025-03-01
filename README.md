# HEIF to JPEG Converter
A high-performance Python utility for batch converting HEIF/HEIC images to JPEG format with parallel processing capabilities.

## Features

- Parallel image processing using ProcessPoolExecutor
- Maintains aspect ratio while resizing
- Progress bar with real-time status
- Comprehensive logging
- Configurable image quality and size limits

## Requirements
``` plaintext
pyenv with Python 3.12.9
pipenv
---
Pillow
pillow-heif
colorlog
```

## Installation
```bash
git clone https://github.com/priesdelly/python-hif2jpg
cd python-hif2jpg
pipenv install
```

## Usage

1. Rename `.env.example` to `.env` and update config
```env
INPUT_DIRECTORY="/Camera/event1-input"
OUTPUT_DIRECTORY="/Camera/event1-output"
```
2. Run the script:
```bash
pipenv run python -m main
```
## Author
Priesdelly

## Acknowledgments
- pillow-heif library maintainers
- PIL/Pillow team