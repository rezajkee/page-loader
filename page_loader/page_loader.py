__all__ = ["download"]
import os
from page_loader.app_logger import get_logger
from page_loader.file_actions import open_page, save_page, create_directory
from page_loader.resources import get_resources, handling_resources
from progress.bar import ChargingBar

logger = get_logger(__name__)


class KnownException(Exception):
    pass


TIMEOUT = 20
CHUNK_SIZE = 8192
TAGS = {
    "img": "src",
    "link": "href",
    "script": "src",
}


def download(url, path):
    logger.info(f"requested url: {url}")
    logger.info(f"output path: {os.path.abspath(path)}")
    page = open_page(url)
    soup, finded_links = get_resources(page, url)
    page_abspath = save_page(url, path, soup)
    logger.info(f"write html file: {page_abspath}")
    if finded_links:
        dir_abs_path = create_directory(url, path)
        bar = ChargingBar(
            'Downloading: ', max=len(finded_links), suffix='%(percent)d%%'
        )
        for link, _attr in finded_links:
            handling_resources(link, _attr, url, dir_abs_path)
            bar.next()
        bar.finish()
    return page_abspath
