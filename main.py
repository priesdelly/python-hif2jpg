import os
from concurrent.futures import ProcessPoolExecutor
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import List, Tuple
from pillow_heif import register_heif_opener
from PIL import Image
import colorlog

# Register HEIF support
register_heif_opener()

# Configuration
input_directory = os.getenv("INPUT_DIRECTORY")
output_directory = os.getenv("OUTPUT_DIRECTORY")
max_img_size = int(os.getenv("MAX_IMG_SIZE"))


# Setup logging
def setup_logging():
    log_queue = Queue()
    queue_handler = QueueHandler(log_queue)
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(queue_handler)

    listener = QueueListener(log_queue, handler)
    listener.start()


def validate_input() -> List[str]:
    errors = []

    if not input_directory:
        errors.append("Input directory is not set")
    if not output_directory:
        errors.append("Output directory is not set")
    if not max_img_size:
        errors.append("Max image size is not set")
    if not os.path.isdir(input_directory):
        errors.append("Input directory does not exist")
    if not os.path.isdir(output_directory):
        errors.append("Output directory does not exist")

    return errors


def convert_and_resize(input_path: str, output_path: str) -> bool:
    try:
        with Image.open(input_path) as image:

            # Resize image while maintaining aspect ratio
            image.thumbnail((max_img_size, max_img_size))

            # Save as JPG
            image.convert("RGB").save(
                output_path, "JPEG", quality=95, optimize=True, progressive=True
            )

            return True
    except Exception as e:
        logging.error(f"Failed to process {input_path}: {e}")
        return False


def get_heif_files(input_directory: str) -> List[str]:
    heif_files = []

    for filename in os.listdir(input_directory):
        if filename.lower().endswith(("heic", "heif", "hif")):
            heif_files.append(os.path.join(input_directory, filename))
    return heif_files


def process_file(file_input_path: str) -> Tuple[str, bool]:
    file_name = os.path.basename(file_input_path)
    file_output_path = os.path.join(
        output_directory, os.path.splitext(file_name)[0] + ".jpg"
    )

    # Convert and resize image
    success = convert_and_resize(file_input_path, file_output_path)
    return file_name, success


def main():
    setup_logging()
    logging.info("Init conversion...")
    logging.info("Validate input...")
    errors = validate_input()
    if errors:
        for error in errors:
            logging.error(error)
        return

    logging.info(f"Input directory: {input_directory}")
    logging.info(f"Output directory: {output_directory}")
    logging.info(f"Max image size: {max_img_size}")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    heif_files = get_heif_files(input_directory)
    heif_file_count = len(heif_files)
    item_processed = 0
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:

        futures = {
            executor.submit(process_file, file_input_path): file_input_path
            for file_input_path in heif_files
        }

        for future in futures:
            file_name, success = future.result()

            item_processed += 1
            percent = int(item_processed * 100 / heif_file_count)

            logging.info(
                f"Processing ({item_processed}/{heif_file_count}) [{percent}%]: {file_name}"
            )

            if not success:
                logging.error(f"Failed to process {file_name}")

    logging.info("Conversion completed")


if __name__ == "__main__":
    main()
