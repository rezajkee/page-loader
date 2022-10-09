#!/usr/bin/env python

import sys

from page_loader.cli import parse_args
from page_loader.page_loader import KnownException, download


def main():
    args = parse_args()
    try:
        saved_page_path = download(args.url_to_download, args.output)
        print(f"Page was downloaded as '{saved_page_path}'")
    except KnownException:
        sys.exit(1)


if __name__ == "__main__":
    main()
