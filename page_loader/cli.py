import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument(
        '-out', '--output',
        default=os.getcwd(),
        help='set path to the existing directory (current directory by default)'
    )
    parser.add_argument('url_to_download', type=str)
    return parser.parse_args()
