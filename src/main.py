#!/usr/bin/env python3

from requests_html import HTMLSession
from sys import exit, argv

def show_help():
    print("""Packt E-Book Importer: Version 0.0.1
    -h | --help \tShow this help message

    Usage:

    ./main.py "MyCookie=123123"

    Arguments:

    <cookies>\tCookies from a logged session in your browser
""")

def validate_args():
    if len(argv) != 2 or (argv[1] == "-h" or argv[1] == "--help"):
        show_help()
        exit(1)
    
    return argv[1]

def fetch_books(cookie):
    # session = HTMLSession()

    values = (item.trim().split('=') for item in cookie.split(';'))

    for value in values:
        print(value)

    # session.cookies.set()


def main():
    cookie = validate_args()
    fetch_books(cookie)


if __name__ == '__main__':
    main()
