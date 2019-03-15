#! /usr/bin/env python3
# Time-stamp: <2019-03-15 14:41:30 christophe@pallier.org>

""" Estimate sublexical statistics from the four files '{english,french}-freq{books,films}.csv' and save them in pickle files:

    french-freqfilms.sublexstats
    french-freqbooks.sublexstats
    english-freqfilms.sublexstats
    english-freqbooks.sublexstats

"""

from sublexstats import sublexstats

en_books = sublexstats()
en_books.import_csv('english-freqbooks.csv', caching=True)

en_films = sublexstats()
en_films.import_csv('english-freqfilms.csv', caching=True)

fr_books = sublexstats()
fr_books.import_csv('french-freqbooks.csv', caching=True)

fr_films = sublexstats()
fr_films.import_csv('french-freqfilms.csv', caching=True)
