__all__ = ["download"]
import requests
import os
import re
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
from page_loader.app_logger import get_logger
from progress.bar import ChargingBar

logger = get_logger(__name__)


class KnownException(Exception):
    pass


TIMEOUT = 20
CHUNK_SIZE = 8192


def download(url, path):
    parsed_page_url = urlsplit(url)
    name_from_url = make_name(parsed_page_url)
    logger.info(f"requested url: {url}")
    logger.info(f"output path: {os.path.abspath(path)}")
    html_file_path = save_page_to_file(url, path, name_from_url)
    logger.info(f"write html file: {html_file_path}")
    dir_abs_path = make_dir(name_from_url, path)
    try:
        with open(html_file_path, "r") as fr:
            soup = BeautifulSoup(fr, "html.parser")
            img_tags = soup.find_all("img", src=True)
            link_tags = soup.find_all("link", href=True)
            script_tags = soup.find_all("script", src=True)
            value_of_iterations = (
                len(img_tags)
                + len(link_tags)
                + len(script_tags)
            )
            bar = ChargingBar(
                'Downloading: ', max=value_of_iterations, suffix='%(percent)d%%'
            )
            if img_tags:
                dwl_cont_mod_html(
                    soup, parsed_page_url, dir_abs_path, "img", "src", bar
                )
            if link_tags:
                dwl_cont_mod_html(
                    soup, parsed_page_url, dir_abs_path, "link", "href", bar
                )
            if script_tags:
                dwl_cont_mod_html(
                    soup, parsed_page_url, dir_abs_path, "script", "src", bar
                )
            with open(html_file_path, "w") as fw:
                print(soup.prettify(), file=fw, end="")
    except PermissionError as e:
        logger.debug(f'Recieved an error {e} when creating a file')
        logger.error(
            f"Can't create '{html_file_path}' – no permission to directory"
        )
        raise KnownException() from e
    bar.finish()
    return html_file_path


def make_name(parsed_url):
    path = parsed_url.path
    pattern = r"(.+?)(?:\.\w*)?$"
    path_without_exe = re.search(pattern, path).group(1)
    raw_name = parsed_url.netloc + path_without_exe
    new_name = re.sub(r"\W", "-", raw_name)
    logger.debug(f"Get name '{new_name}' from path: '{path}'")
    return new_name


def save_page_to_file(url, path, name):
    file_name = name + ".html"
    new_file_path = os.path.join(path, file_name)
    try:
        with requests.get(url, timeout=TIMEOUT) as response:
            response.raise_for_status()
            html = response.text
        with open(new_file_path, "w") as f:
            print(html, file=f, end="")
    except requests.exceptions.HTTPError as e:
        logger.debug(f'Request to url get error {e}')
        logger.error(f"Bad status code – {e}")
        raise KnownException() from e
    except PermissionError as e:
        logger.debug(f'Recieved an error {e} when creating a file')
        logger.error(
            f"Can't create '{new_file_path}' – no permission to directory"
        )
        raise KnownException() from e
    return os.path.abspath(new_file_path)


def make_dir(name, path):
    dir_name = name + "_files"
    new_dir_path = os.path.join(path, dir_name)
    try:
        os.mkdir(new_dir_path)
    except OSError as e:
        logger.debug(f'Recieved an error {e} when creating the directory')
        logger.error(
            f"Directory '{dir_name}' already exist"
            f" or no permission to create it"
        )
        raise KnownException() from e
    return os.path.abspath(new_dir_path)


def dwl_cont_mod_html(soup, parsed_page_url, dir_abs_path, _tag, _attr, bar):
    files_dir_name = os.path.basename(dir_abs_path)
    for tag in soup.find_all(_tag, attrs={_attr: True}):
        content_url = urlsplit(tag[_attr])
        if content_url.netloc and content_url.netloc != parsed_page_url.netloc:
            bar.next()
            continue
        else:
            content_url = parsed_page_url._replace(
                path=content_url.path,
                query=content_url.query,
                fragment=content_url.fragment,
            )
            new_cont_name = make_name(content_url)
            if len(content_url.path.split(".")) > 1:
                new_cont_name = (
                    new_cont_name + "." + content_url.path.split(".")[-1]
                )
            if len(content_url.path.split(".")) == 1 and _attr == "href":
                html_path = save_page_to_file(
                    urlunsplit(content_url), dir_abs_path, new_cont_name
                )
                tag[_attr] = os.path.join(
                    files_dir_name, os.path.basename(html_path)
                )
                bar.next()
                continue
            cont_abs_path = os.path.join(dir_abs_path, new_cont_name)
            get_content(urlunsplit(content_url), cont_abs_path)
            tag[_attr] = os.path.join(files_dir_name, new_cont_name)
            bar.next()
    return soup


def get_content(content_url, path):
    try:
        with requests.get(
            content_url, stream=True, timeout=TIMEOUT
        ) as response:
            response.raise_for_status()
            chunked_content = response.iter_content(CHUNK_SIZE)
            with open(path, "bw") as f:
                for chunk in chunked_content:
                    f.write(chunk)
    except requests.exceptions.HTTPError as e:
        logger.debug(f'Request to url recieved an error {e}')
        logger.error(f"Bad status code – {e}")
        raise KnownException() from e
    except PermissionError as e:
        logger.debug(f'Recieved an error {e} when creating a file')
        logger.error(f"Can't create '{path}' – no permission to directory")
        raise KnownException() from e
