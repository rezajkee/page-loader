import re
from urllib.parse import urlsplit


def create_name(url):
    parsed_page_url = urlsplit(url)
    url_path = parsed_page_url.path
    re_pattern = r"(.+?)(?:\.\w*)?$"
    path_without_exe = re.search(re_pattern, url_path).group(1)
    raw_name = parsed_page_url.netloc + path_without_exe
    new_name = re.sub(r"\W", "-", raw_name)
    return new_name
