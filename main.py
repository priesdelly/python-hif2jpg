import os
from concurrent.futures import ProcessPoolExecutor
import logging
from typing import List, Tuple
from pillow_heif import register_heif_opener
from PIL import Image
from tqdm import tqdm

# Register HEIF support
register_heif_opener()

# Configuration
input_directory = "/Camera/event1-input"
output_directory = "/Camera/event1-output"
max_img_size = 4096


# Setup logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("conversion.log")],
    )


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

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    heif_files = get_heif_files(input_directory)
    heif_file_count = len(heif_files)

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        with tqdm(total=heif_file_count) as pbar:

            futures = {
                executor.submit(process_file, file_input_path): file_input_path
                for file_input_path in heif_files
            }

            for future in futures:
                file_name, success = future.result()

                # Update progress bar description
                pbar.set_description(f"Processing {file_name}")

                # Update progress bar
                pbar.update(1)

                if not success:
                    logging.error(f"Failed to process {file_name}")


if __name__ == "__main__":
    main()
