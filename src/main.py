#!/usr/bin/env python3

from requests_html import HTMLSession
from sys import exit, argv

preference_order = ['mobi', 'epub', 'pdf']


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


def create_session(cookie):
    session = HTMLSession()

    cookie_values = (item.split('=') for item in cookie.split(';'))

    for cookie_value in cookie_values:
        session.cookies.set(cookie_value[0], cookie_value[1])

    return session


def get_download_link(ebook):
    for download_link, ebooktype in ((ebook.find(".download-container a[href$={}]".format(o)), o) for o in
                                     preference_order):
        if len(download_link) != 0:
            return download_link[0].attrs["href"], ebooktype

    raise Exception('Failed to get a download link for ebook: ' + ebook.attrs["title"])


def fetch_books(session):
    print('Fetching page...')
    response = session.get("https://www.packtpub.com/account/my-ebooks")

    print('Parsing it...')
    ebooks = response.html.find(".product-line[nid]")

    for ebook in ebooks:
        download_link, ebook_type = get_download_link(ebook)
        yield {
            'name': ebook.attrs["title"].replace(' [eBook]', ''),
            'url': 'https://www.packtpub.com/' + download_link,
            'type': ebook_type
        }


def count_by_type(ebooks, type):
    """
    Count the amount of occurrences in ebooks dict
    :rtype: int
    """
    amount = 0
    for ebook in ebooks:
        if ebook['type'] == type:
            amount += 1
    return amount


def print_summary(ebooks):
    if len(ebooks) == 0:
        print('Nothing to download :(')
    else:
        print('Found {} ebooks!'.format(len(ebooks)))
        print('Mobi: {}\tEpub: {}\tPdf: {}'.format(
            count_by_type(ebooks, 'mobi')
            , count_by_type(ebooks, 'epub')
            , count_by_type(ebooks, 'pdf')
        ))
    pass


def save_to_disk(session, ebooks):
    len_ebooks = len(ebooks)
    i = 0

    # TODO: Add some parallelization here
    for ebook in ebooks:
        i += 1
        print('Downloading {}/{}\t{}...'.format(i, len_ebooks, ebook['name']))
        r = session.get(ebook['url'])
        with open(ebook['name'] + '.' + ebook['type'], 'wb') as fd:
            for chunk in r.iter_content(chunk_size=2048):
                fd.write(chunk)


def main():
    cookie = validate_args()
    session = create_session(cookie)
    ebooks = list(fetch_books(session))
    print_summary(ebooks)
    save_to_disk(session, ebooks)
    print('Done :)')


if __name__ == '__main__':
    main()
