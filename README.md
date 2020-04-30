# free-books
Elsevier and Springer have made available free books because of the COVID-19 pandemia. This script makes easy to search for books and to download them

Python 3 is needed. Installation is as easy as downloading the script and having installed the following modules:

* pandas
* urllib3
* beautifulsoup4

The script has fundamentally two uses:

## Searching

In order to search a book, the instruction is:

```shell
python free-books.py -s '.*Artificial.*'
```

Then, the script return the following lines:

```shell
Searching for books that match the regular expression...

* Elsevier matches:

                                  Book Title  Year          Imprint
11  Artificial Intelligence: A New Synthesis  1998  Morgan Kaufmann

* Springer matches:

                                  Book Title  Copyright Year          Author
301  Introduction to Artificial Intelligence            2017  Wolfgang Ertel
```

## Downloading

Once we know the index of the book we want to download, we only have to use the instruction as follows:

```shell
python free-books.py -d s301
```

If the index starts with an *s*, then the books comes from the Springer library. Elsevier downloads still not implemented *Coming soon*.