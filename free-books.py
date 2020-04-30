#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import re
import argparse
import pandas as pd
import urllib3 as urllib
from bs4 import BeautifulSoup

def parse_arguments():
    parser = argparse.ArgumentParser(description='\
This program makes easier to search and download\
the books that both Elsevier and Springer have made\
available for free because of the COVID-19 pandemia.\
')
    parser.add_argument('-s', '--search',\
                        help='Search a book with regular expressions', \
                        action='store')
    parser.add_argument('-d', '--download',\
                        help='Download books passing the with regular expressions', \
                        action='store', nargs = max(1,(len(sys.argv) - 2)))
    args = parser.parse_args()
    return args

def search(args):
    print('Searching for books that match the regular expression...')
    data_elsevier = pd.read_csv('elsevier-books.csv', sep=';')
    df_elsevier = data_elsevier[data_elsevier['Book Title'].str.match(r'{}'.format(args))]
    if len(df_elsevier):
        print('\n* Elsevier matches:\n')
        print(df_elsevier[['Book Title', 'Year', 'Imprint']])
    data_springer = pd.read_csv('springer-books.csv', sep=';')
    df_springer = data_springer[data_springer['Book Title'].str.match(r'{}'.format(args))]
    if len(df_springer):
        print('\n* Springer matches:\n')
        print(df_springer[['Book Title', 'Copyright Year', 'Author']])

def download(args):
    for index in args:
        if index.startswith('s'):
            print('Springer book')
            index = int(index[1:])
            download_springer(index)
        elif index.startswith('e'):
            print('Elsevier book')
            index = int(index[1:])
            download_elsevier(index)

def download_springer(index):
    data_springer = pd.read_csv('springer-books.csv', sep=';')
    if index < len(data_springer):
        book = data_springer.loc[index]
        print('Downloading {}...'.format(book['Book Title']))
        url = book['OpenURL']
        http = urllib.PoolManager()
        response = http.request('GET', url)
        html = BeautifulSoup(response.data, features='html.parser')
        div_book = html.findAll('a', {'class' : 'test-bookpdf-link'})[0]
        url_book = div_book['href']
        url_book = 'https://link.springer.com' + url_book
        filename = '{}.pdf'.format(book['Book Title'])
        response.release_conn()
        r = http.request('GET', url_book, preload_content=False)
        with open(filename, 'wb') as out:
            while True:
                data = r.read()
                if not data:
                    break
                out.write(data)
        r.release_conn()
    else:
        print('Not found')
    pass

def download_elsevier(index):
    data_elsevier = pd.read_csv('elsevier-books.csv', sep=';')
    pass

if __name__ == '__main__':
    args = parse_arguments()
    if args.search:
        search(sys.argv[2])
    elif args.download:
        download(sys.argv[2:])
    else:
        print('Please, use free-books.py -h for more help.')


