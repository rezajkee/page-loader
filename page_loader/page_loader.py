__all__ = ['download']
import requests
import os
import re
from urllib.parse import urlparse


def make_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    pattern = r'(.+?)(?:\.\w*)?$'
    path_without_exe = re.search(pattern, path)[1]
    raw_name = parsed_url.netloc + path_without_exe
    new_name = re.sub(r'\W', '-', raw_name)
    return new_name


def download(url, path):
    file_name = make_name(url) + ".html"
    new_file_path = os.path.join(path, file_name)
    with requests.get(url) as response:
        html = response.text
        with open(new_file_path, "w") as f:
            print(html, file=f)
    return os.path.abspath(new_file_path)

# download("http://httpbin.org/", os.getcwd())
# page-loader http://httpbin.org/
# page-loader --output some/body http://httpbin.org/
