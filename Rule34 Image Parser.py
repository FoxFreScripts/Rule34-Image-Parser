import os
import json
import threading
import random
import httpx
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from art import text2art
from colorama import Fore, Style, init

# Initialize colorama
init()

# Print a smaller cool text banner
banner_text = text2art("Rule34 Image Parser", font='small')
print(banner_text)

# ANSI escape codes for yellowish-orange color
warning_color = Fore.YELLOW
reset_color = Style.RESET_ALL

# Request settings
endpoint_url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=%s&json=1&limit=1000&pid=%s"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

# Read tags from tags.json
with open('tags.json', 'r') as tags_file:
    tags_data = json.load(tags_file)
    tags = tags_data.get("tags", [])

# Create a string with all the tags with either "+" or "-" for rule34 api
formatted_tags = "".join("+" + i for i in tags)

# Print warnings with yellowish-orange color
print(f"\n{warning_color}WARNING: Please be cautious with the number of images you choose to download.{reset_color}")
print(f"{warning_color}Fetching many images might take some time.{reset_color}")
print(f"{warning_color}This script downloads images very quickly. To stop downloading, simply close the console.{reset_color}")

# Prompt the user for the limit
limit = int(input("Enter the number of images to download: "))

# Inform the user that images are being generated
print("Please wait...")

# Fetch more image links using the provided endpoint URL and formatted tags
response = httpx.get(endpoint_url % (formatted_tags, 0), headers=headers)
if response.status_code == 200:
    json_data = response.json()
    all_images_links = [post['file_url'] for post in json_data]

    # Shuffle the list of all image links for randomness
    random.shuffle(all_images_links)

    # Select the desired number of images randomly
    selected_images = all_images_links[:limit]

    # Create a folder named 'PO' if it doesn't exist
    folder_path = 'PO_N'
    os.makedirs(folder_path, exist_ok=True)

    # Download and save images with multi-threading
    def download_image(image_index, image_link):
        try:
            image_url = urljoin(endpoint_url, image_link)
            with httpx.stream("GET", image_url, headers=headers, timeout=5) as response:
                if response.status_code == 200:
                    # Extract image name from the URL or use a default name
                    image_name = os.path.basename(image_url) or f"image_{image_index}.jpg"
                    image_path = os.path.join(folder_path, image_name)

                    # Download and save the image
                    with open(image_path, 'wb') as image_file:
                        image_file.write(response.read())

                    print(f"Downloaded: {image_name}")
                else:
                    print(f"Failed to download image {image_index}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image {image_index}: {str(e)}")

    # Download and save images with multi-threading
    with ThreadPoolExecutor(max_workers=15) as executor:
        for image_index, image_link in enumerate(selected_images):
            executor.submit(download_image, image_index + 1, image_link)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
