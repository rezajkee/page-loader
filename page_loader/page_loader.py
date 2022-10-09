__all__ = ["download"]

import os

from page_loader.app_logger import get_logger
from page_loader.file_actions import create_directory, get_page, save_page
from page_loader.resources import download_assets, get_resources
from progress.bar import ChargingBar

logger = get_logger(__name__)


class KnownException(Exception):
    pass


def download(url, path):
    logger.info(f"requested url: {url}")
    logger.info(f"output path: {os.path.abspath(path)}")
    page = get_page(url)
    soup, found_links = get_resources(page, url)
    page_abspath = save_page(url, path, soup)
    logger.info(f"write html file: {page_abspath}")
    if found_links:
        dir_abs_path = create_directory(url, path)
        bar = ChargingBar(
            "Downloading: ", max=len(found_links), suffix="%(percent)d%%"
        )
        for link, _attr in found_links:
            download_assets(link, _attr, url, dir_abs_path)
            bar.next()
        bar.finish()
    return page_abspath
