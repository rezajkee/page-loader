import os
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup, ResultSet
from page_loader.file_actions import get_page, save_content, save_page
from page_loader.name_creator import create_name

TAGS = {
    "img": "src",
    "link": "href",
    "script": "src",
}


def get_resources(page, page_url):
    soup = BeautifulSoup(page, "html.parser")
    found_elements = ResultSet(soup)
    for _tag, _attr in TAGS.items():
        found_elements.extend(soup.find_all(_tag, attrs={_attr: True}))
    found_links = []
    for elem in found_elements:
        _attr = TAGS[elem.name]
        splitted_link = urlsplit(elem[_attr])
        splitted_page_url = urlsplit(page_url)
        if is_local(splitted_link, splitted_page_url):
            found_links.append((elem[_attr], _attr))
            elem[_attr] = modify_link(splitted_link, splitted_page_url, _attr)
    return soup.prettify(), found_links


def is_local(splitted_link, splitted_page_url):
    if (
        splitted_link.netloc
        and splitted_link.netloc != splitted_page_url.netloc
    ):
        return False
    else:
        return True


def modify_link(splitted_link, splitted_page_url, _attr):
    full_link, splitted_full_link = make_full_and_splitted_full_links(
        splitted_page_url, splitted_link
    )
    new_cont_name = create_name(full_link)
    if len(splitted_full_link.path.split(".")) > 1:
        new_cont_name = (
            new_cont_name + "." + splitted_full_link.path.split(".")[-1]
        )
    if len(splitted_full_link.path.split(".")) == 1 and _attr == "href":
        new_cont_name = new_cont_name + ".html"
    files_dir_name = create_name(urlunsplit(splitted_page_url)) + "_files"
    return os.path.join(files_dir_name, new_cont_name)


def download_assets(link, _attr, page_url, dir_abs_path):
    splitted_link = urlsplit(link)
    splitted_page_url = urlsplit(page_url)

    full_link, splitted_full_link = make_full_and_splitted_full_links(
        splitted_page_url, splitted_link
    )

    if len(splitted_full_link.path.split(".")) == 1 and _attr == "href":
        save_page(full_link, dir_abs_path, get_page(full_link))
        return

    new_cont_name = create_name(full_link)
    if len(splitted_full_link.path.split(".")) > 1:
        new_cont_name = (
            new_cont_name + "." + splitted_full_link.path.split(".")[-1]
        )
    cont_abs_path = os.path.join(dir_abs_path, new_cont_name)
    save_content(full_link, cont_abs_path)


def make_full_and_splitted_full_links(splitted_page_url, splitted_link):
    splitted_full_link = splitted_page_url._replace(
        path=splitted_link.path,
        query=splitted_link.query,
        fragment=splitted_link.fragment,
    )
    full_link = urlunsplit(splitted_full_link)
    return full_link, splitted_full_link
