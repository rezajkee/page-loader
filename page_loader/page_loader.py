__all__ = ['download']
import requests
import os
import re
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup


def download(url, path):
    name_from_url = make_name(url)
    html_file_path = get_html(url, path, name_from_url)
    dir_abs_path = make_dir(name_from_url, path)
    dwl_pics_mod_html(url, html_file_path, dir_abs_path)
    print(html_file_path)


def make_name(url):
    parsed_url = urlsplit(url)
    path = parsed_url.path
    pattern = r'(.+?)(?:\.\w*)?$'
    path_without_exe = re.search(pattern, path)[1]
    raw_name = parsed_url.netloc + path_without_exe
    new_name = re.sub(r'\W', '-', raw_name)
    return new_name


def get_html(url, path, name):
    file_name = name + ".html"
    new_file_path = os.path.join(path, file_name)
    with requests.get(url) as response:
        html = response.text
        with open(new_file_path, "w") as f:
            print(html, file=f)
    return os.path.abspath(new_file_path)


def make_dir(name, path):
    dir_name = name + "_files"
    new_dir_path = os.path.join(path, dir_name)
    os.mkdir(new_dir_path)
    return os.path.abspath(new_dir_path)


def dwl_pics_mod_html(url_to_page, path_to_html, dir_abs_path):
    with open(path_to_html, 'r') as fr:
        soup = BeautifulSoup(fr, 'html.parser')
        if not soup.find('img'):
            pass
        else:
            for tag in soup.find_all('img'):
                page_url = urlsplit(url_to_page)
                pic_url = urlsplit(tag['src'])
                if pic_url.netloc:
                    pass
                pic_url = page_url._replace(path=pic_url.path, query=pic_url.query, fragment=pic_url.fragment)
                if len(pic_url.path.split('.')) > 1:
                    new_pic_name = make_name(urlunsplit(pic_url)) + '.' + pic_url.path.split('.')[-1]
                pic_abs_path = os.path.join(dir_abs_path, new_pic_name)
                get_pic(urlunsplit(pic_url), pic_abs_path)
                tag['src'] = os.path.join(os.path.basename(dir_abs_path), new_pic_name)
            with open(path_to_html, 'w') as fw:
                print(soup.prettify(), file=fw)


def get_pic(url, path):
    with requests.get(url, stream=True) as response:
        chunked_content = response.iter_content(8192)
        with open(path, 'bw') as f:
            for chunk in chunked_content:
                f.write(chunk)

# download("http://httpbin.org/", os.getcwd())
# page-loader http://httpbin.org/
# page-loader --output body/once https://toolster.net/browser_checker
