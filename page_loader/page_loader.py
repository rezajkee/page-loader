__all__ = ["download"]
import requests
import os
import re
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup


def download(url, path):
    parsed_page_url = urlsplit(url)
    name_from_url = make_name(parsed_page_url)
    html_file_path = get_html(url, path, name_from_url)
    dir_abs_path = make_dir(name_from_url, path)
    with open(html_file_path, "r") as fr:
        soup = BeautifulSoup(fr, "html.parser")
        if soup.find_all("img", src=True):
            dwl_cont_mod_html(soup, parsed_page_url, dir_abs_path, "img", "src")
        if soup.find_all("link", href=True):
            dwl_cont_mod_html(
                soup, parsed_page_url, dir_abs_path, "link", "href"
            )
        if soup.find_all("script", src=True):
            dwl_cont_mod_html(
                soup, parsed_page_url, dir_abs_path, "script", "src"
            )
        with open(html_file_path, "w") as fw:
            print(soup.prettify(), file=fw)
    return html_file_path


def make_name(parsed_url):
    path = parsed_url.path
    pattern = r"(.+?)(?:\.\w*)?$"
    path_without_exe = re.search(pattern, path)[1]
    raw_name = parsed_url.netloc + path_without_exe
    new_name = re.sub(r"\W", "-", raw_name)
    return new_name


def get_html(url, path, name):
    file_name = name + ".html"
    new_file_path = os.path.join(path, file_name)
    with requests.get(url) as response:
        html = response.text
        with open(new_file_path, "w") as f:
            print(html, file=f, end="")
    return os.path.abspath(new_file_path)


def make_dir(name, path):
    dir_name = name + "_files"
    new_dir_path = os.path.join(path, dir_name)
    os.mkdir(new_dir_path)
    return os.path.abspath(new_dir_path)


def dwl_cont_mod_html(soup, parsed_page_url, dir_abs_path, _tag, _attr):
    files_dir_name = os.path.basename(dir_abs_path)
    for tag in soup.find_all(_tag, attrs={_attr: True}):
        cont_url = urlsplit(tag[_attr])
        if cont_url.netloc and cont_url.netloc != parsed_page_url.netloc:
            pass
        else:
            cont_url = parsed_page_url._replace(
                path=cont_url.path,
                query=cont_url.query,
                fragment=cont_url.fragment,
            )
            new_cont_name = make_name(cont_url)
            if len(cont_url.path.split(".")) > 1:
                new_cont_name = (
                    new_cont_name + "." + cont_url.path.split(".")[-1]
                )
            if len(cont_url.path.split(".")) == 1 and _attr == "href":
                html_path = get_html(
                    urlunsplit(cont_url), dir_abs_path, new_cont_name
                )
                tag[_attr] = os.path.join(
                    files_dir_name, os.path.basename(html_path)
                )
                continue
            cont_abs_path = os.path.join(dir_abs_path, new_cont_name)
            get_cont(urlunsplit(cont_url), cont_abs_path)
            tag[_attr] = os.path.join(files_dir_name, new_cont_name)
    return soup


def get_cont(cont_url, path):
    with requests.get(cont_url, stream=True) as response:
        chunked_content = response.iter_content(8192)
        with open(path, "bw") as f:
            for chunk in chunked_content:
                f.write(chunk)
