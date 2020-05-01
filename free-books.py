#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys, os
import argparse
import shutil
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
    data_elsevier = pd.read_csv('elsevier-books.csv', sep=';', encoding='utf-8')
    df_elsevier = data_elsevier[data_elsevier['Book Title'].str.match(r'{}'.format(args))]
    if len(df_elsevier):
        print('\n* Elsevier matches:\n')
        print(df_elsevier[['Book Title', 'Year', 'Imprint']])
    data_springer = pd.read_csv('springer-books.csv', sep=';', encoding='utf-8')
    df_springer = data_springer[data_springer['Book Title'].str.match(r'{}'.format(args))]
    if len(df_springer):
        print('\n* Springer matches:\n')
        print(df_springer[['Book Title', 'Copyright Year', 'Author']])

def download(args):
    try:
        os.mkdir('output')
    except:
        pass
    for index in args:
        if index.startswith('s'):
            index = int(index[1:])
            download_springer(index)
        elif index.startswith('e'):
            index = int(index[1:])
            download_elsevier(index)

def download_springer(index):
    data_springer = pd.read_csv('springer-books.csv', sep=';')
    if index < len(data_springer):
        book = data_springer.loc[index]
        print('Downloading {}'.format(book['Book Title']), end='', flush=True)
        url = book['OpenURL']
        http = urllib.PoolManager()
        response = http.request('GET', url)
        print('.', end='', flush=True)
        html = BeautifulSoup(response.data, features='html.parser')
        div_book = html.findAll('a', {'class' : 'test-bookpdf-link'})[0]
        url_book = div_book['href']
        print('.', end='', flush=True)
        url_book = 'https://link.springer.com' + url_book
        filename = 'output/{}.pdf'.format(book['Book Title'])
        response.release_conn()
        r = http.request('GET', url_book, preload_content=False)
        print('.', end='', flush=True)
        with open(filename, 'wb') as out:
            shutil.copyfileobj(r, out)
        r.release_conn()
        print(' Complete!')
    else:
        print('Not found')
    pass

def download_elsevier(index):
    data_elsevier = pd.read_csv('elsevier-books.csv', sep=';')
    if index < len(data_elsevier):
        book = data_elsevier.loc[index]
        url = book['URL']
        title = book['Book Title']
        print('The URL of the book', title, 'is', url)
    else:
        print('Not found')

if __name__ == '__main__':
    args = parse_arguments()
    if args.search:
        search(sys.argv[2])
    elif args.download:
        download(sys.argv[2:])
    else:
        print('Please, use free-books.py -h for more help.')


