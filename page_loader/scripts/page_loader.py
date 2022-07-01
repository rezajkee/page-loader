#!/usr/bin/env python

import sys
from page_loader.page_loader import download, KnownException
from page_loader.cli import parse_args


def main():
    args = parse_args()
    try:
        download(args.url_to_download, args.output)
    except KnownException:
        sys.exit(1)


if __name__ == "__main__":
    main()
