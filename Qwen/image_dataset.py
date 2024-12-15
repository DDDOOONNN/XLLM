import base64
import logging
import os
import re

# SPAQ dir_path: /data/IQA-Dataset/SPAQ/TestImage
image_dir_path = "/data/IQA-Dataset/SPAQ/TestImage"
path_cache = {}

def get_image_path_SPAQ(image_dir_path, image_name):
    key = (image_dir_path, image_name)
    if key in path_cache:
        return path_cache[key]

    try:
        if not image_dir_path or not image_name:
            raise ValueError("image_dir_path and image_name must be non-empty strings")

        image_path = os.path.normpath(os.path.join(image_dir_path, image_name))
        path_cache[key] = image_path
        return image_path
    except (OSError, ValueError) as e:
        print(f"Error: {e}")
        return None

# Function to list all image paths in the directory
def list_image_paths_SPAQ(directory):
    image_paths = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            image_path = get_image_path_SPAQ(directory, filename)
            if image_path:
                image_paths.append(image_path)
    # Sort the image paths based on the numerical part of the filename
    image_paths.sort(key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))
    return image_paths

def encode_image(image_path):
    """
    Encode an image file to Base64 data URI format.
    """
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        img_data_uri = f"data:image/jpeg;base64,{img_b64}"
        return img_data_uri
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        raise e

# Get all image paths in the specified directory
all_image_paths = list_image_paths_SPAQ(image_dir_path)

# # Get the first 5 image paths
# first_5_image_paths = all_image_paths[:5]

# # Example usage: Print the first 5 image paths and their Base64 encoding
# for image_path in first_5_image_paths:
#     print(image_path)
#     # print(encode_image(image_path))