#!/usr/bin/env python

from page_loader.page_loader import download
from page_loader.cli import parse_args


def main():
    args = parse_args()
    print(download(args.url_to_download, args.output))


if __name__ == "__main__":
    main()
