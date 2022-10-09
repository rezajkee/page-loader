import os

import requests
from page_loader import page_loader
from page_loader.name_creator import create_name

TIMEOUT = 20
CHUNK_SIZE = 8192


def get_page(url):
    try:
        with requests.get(url, timeout=TIMEOUT) as response:
            response.raise_for_status()
            html = response.text
    except requests.exceptions.HTTPError as e:
        page_loader.logger.debug(f"Request to url get error {e}")
        page_loader.logger.error(f"Bad status code – {e}")
        raise page_loader.KnownException() from e
    return html


def save_page(url, path, page):
    file_name = create_name(url) + ".html"
    new_file_path = os.path.join(path, file_name)
    try:
        with open(new_file_path, "w") as f:
            print(page, file=f, end="")
    except PermissionError as e:
        page_loader.logger.debug(f"Received an error {e} when creating a file")
        page_loader.logger.error(
            f"Can't create '{new_file_path}' – no permission to directory"
        )
        raise page_loader.KnownException() from e
    return os.path.abspath(new_file_path)


def create_directory(url, path):
    dir_name = create_name(url) + "_files"
    new_dir_path = os.path.join(path, dir_name)
    try:
        os.mkdir(new_dir_path)
    except OSError as e:
        page_loader.logger.debug(
            f"Received an error {e} when creating the directory"
        )
        page_loader.logger.error(
            f"Directory '{dir_name}' already exist"
            f" or no permission to create it"
        )
        raise page_loader.KnownException() from e
    return os.path.abspath(new_dir_path)


def save_content(content_url, name_with_path):
    try:
        with requests.get(
            content_url, stream=True, timeout=TIMEOUT
        ) as response:
            response.raise_for_status()
            chunked_content = response.iter_content(CHUNK_SIZE)
            with open(name_with_path, "bw") as f:
                for chunk in chunked_content:
                    f.write(chunk)
    except requests.exceptions.HTTPError as e:
        page_loader.logger.debug(f"Request to url received an error {e}")
        page_loader.logger.error(f"Bad status code – {e}")
        raise page_loader.KnownException() from e
    except PermissionError as e:
        page_loader.logger.debug(f"Received an error {e} when creating a file")
        page_loader.logger.error(
            f"Can't create '{name_with_path}' – no permission to directory"
        )
        raise page_loader.KnownException() from e
