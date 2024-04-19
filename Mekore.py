import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import argparse
import concurrent.futures
from tqdm import tqdm

def create_unique_folder(base_folder_name):
    folder_name = base_folder_name
    counter = 1
    while os.path.exists(folder_name):
        counter += 1
        folder_name = f"{base_folder_name}_{counter}"
    os.makedirs(folder_name)
    return folder_name

def get_site_name(url):
    parsed_url = urlparse(url)
    site_name = parsed_url.netloc.split('.')[0]
    return site_name

def load_list_from_file(filename):
    items = set()
    if filename and os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                items.add(line.strip())
    return items

def count_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    return len(images)

def download_image(img_url, folder_name, blocked_filenames, allowed_filenames):
    try:
        img_data = requests.get(img_url).content
        filename = os.path.join(folder_name, os.path.basename(img_url))

        # Check if the filename matches any of the blocked filenames
        if any(blocked_filename in filename for blocked_filename in blocked_filenames):
            print(f"Ignoring {filename} due to block list")
            return

        # Check if the filename matches any of the allowed filenames
        if allowed_filenames and not any(allowed_filename in filename for allowed_filename in allowed_filenames):
            print(f"Ignoring {filename} not in allow list")
            return

        # Check if the filename already exists and append a number if it does
        if os.path.exists(filename):
            file_root, file_extension = os.path.splitext(filename)
            counter = 1
            new_filename = f"{file_root}_{counter}{file_extension}"
            while os.path.exists(new_filename):
                counter += 1
                new_filename = f"{file_root}_{counter}{file_extension}"
            filename = new_filename

        with open(filename, 'wb') as file:
            file.write(img_data)
        return True
    except Exception as e:
        print(f"Could not download {img_url}. Reason: {e}")
        return False

def download_images(url, block_list=None, allow_list=None):
    if not url:
        print("No URL provided. Please provide a URL to download images.")
        return

    site_name = get_site_name(url)
    folder_name = create_unique_folder(site_name)

    blocked_filenames = load_list_from_file(block_list)
    allowed_filenames = load_list_from_file(allow_list)

    total_images = count_images(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    img_urls = [urljoin(url, img.attrs.get("src")) for img in images if img.attrs.get("src")]

    with tqdm(total=total_images, desc="Downloading", bar_format="{l_bar}{bar}{r_bar}", ncols=100, colour='green') as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(lambda img_url: download_image(img_url, folder_name, blocked_filenames, allowed_filenames), img_url) for img_url in img_urls]
            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    pbar.update(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from a website")
    parser.add_argument("url", nargs='?', help="URL of the website")
    parser.add_argument("--block_list", help="File containing list of blocked filenames")
    parser.add_argument("--allow_list", help="File containing list of allowed filenames")
    args = parser.parse_args()

    download_images(args.url, block_list=args.block_list, allow_list=args.allow_list)
