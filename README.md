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
Python 3.7+
Pillow
pillow-heif
tqdm
```

## Installation
```bash
git clone https://github.com/yourusername/heif-converter
cd heif-converter
pip install -r requirements.txt
```

## Usage

1. Configure input/output directories in the script:
```python
input_directory = "/Camera/event1-input"
output_directory = "/Camera/event1-output"
```
2. Run the script:
```bash
python main.py
```

## Logging
The script logs all operations to both console and conversion.log file.

## Error Handling
- Failed conversions are logged with error messages
- Script continues processing remaining files if one fails
- Summary of failed files provided upon completion

## License
MIT

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5 .Create a Pull Request

## Author
Priesdelly

## Acknowledgments
- pillow-heif library maintainers
- PIL/Pillow team