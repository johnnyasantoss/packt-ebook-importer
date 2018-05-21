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
    session = HTMLSession()

    cookie_values = (item.split('=') for item in cookie.split(';'))

    for cookie_value in cookie_values:
        session.cookies.set(cookie_value[0], cookie_value[1])

    response = session.get("https://www.packtpub.com/account/my-ebooks")
    ebooks = response.html.find(".product-line")
    i = 0
    for ebook in ebooks:
        i += 1
        print("Importing ebook {%r} {%i}/{%i}".format(ebook.attrs["title"], i,
                                                      len(ebooks)))
        
        mobi_link = ebook.find("a[href~=/mobi]")
        ebook_file = session.get(mobi_link.attrs["href"])
        #TODO: Download mobi file


def main():
    cookie = validate_args()
    fetch_books(cookie)


if __name__ == '__main__':
    main()
