import os
from bs4 import BeautifulSoup, ResultSet
import page_loader.page_loader
from urllib.parse import urlsplit, urlunsplit
from page_loader.name_creator import create_name
from page_loader.file_actions import open_page, save_page, save_content


def get_resources(page, page_url):
    soup = BeautifulSoup(page, "html.parser")
    finded_elements = ResultSet(soup)
    for _tag, _attr in page_loader.page_loader.TAGS.items():
        finded_elements.extend(soup.find_all(_tag, attrs={_attr: True}))
    finded_links = []
    for elem in finded_elements:
        _attr = page_loader.page_loader.TAGS[elem.name]
        splited_link = urlsplit(elem[_attr])
        splited_page_url = urlsplit(page_url)
        if is_local(splited_link, splited_page_url):
            finded_links.append((elem[_attr], _attr))
            elem[_attr] = modify_link(splited_link, splited_page_url, _attr)
    return soup.prettify(), finded_links


def is_local(splited_link, splited_page_url):
    if splited_link.netloc and splited_link.netloc != splited_page_url.netloc:
        return False
    else:
        return True


def modify_link(splited_link, splited_page_url, _attr):
    splited_full_link = splited_page_url._replace(
        path=splited_link.path,
        query=splited_link.query,
        fragment=splited_link.fragment,
    )
    new_cont_name = create_name(urlunsplit(splited_full_link))
    if len(splited_full_link.path.split(".")) > 1:
        new_cont_name = (
            new_cont_name + "." + splited_full_link.path.split(".")[-1]
        )
    if len(splited_full_link.path.split(".")) == 1 and _attr == "href":
        new_cont_name = (
            new_cont_name + ".html"
        )
    files_dir_name = create_name(urlunsplit(splited_page_url)) + "_files"
    return os.path.join(files_dir_name, new_cont_name)


def handling_resources(link, _attr, page_url, dir_abs_path):
    splited_link = urlsplit(link)
    splited_page_url = urlsplit(page_url)
    splited_full_link = splited_page_url._replace(
        path=splited_link.path,
        query=splited_link.query,
        fragment=splited_link.fragment,
    )
    full_link = urlunsplit(splited_full_link)

    if len(splited_full_link.path.split(".")) == 1 and _attr == "href":
        save_page(full_link, dir_abs_path, open_page(full_link))
        return

    new_cont_name = create_name(full_link)
    if len(splited_full_link.path.split(".")) > 1:
        new_cont_name = (
            new_cont_name + "." + splited_full_link.path.split(".")[-1]
        )
    cont_abs_path = os.path.join(dir_abs_path, new_cont_name)
    save_content(full_link, cont_abs_path)
