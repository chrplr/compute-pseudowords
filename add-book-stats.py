#! /usr/bin/env python3
# Time-stamp: <2019-03-15 14:24:07 christophe@pallier.org>

"""
Add sublexical statistics to selected*.csv files
"""


import os
import glob
import pandas as pd
from sublexstats import sublexstats


def process(sfile, fr_books, en_books):
    """Add sublexical stats to a  file.

    Args:
          sfile is a csv file with one columns named 'item'
          fr_books and en_books are both sublexstats objects containing sublexical statistics

    Returns:
          a dataframe corresponding to sfile's content with additional
          columns with french and english sublexical stats
    """

    df = pd.read_csv(sfile)
    frletters_bk, frbigrams_bk, frquadrigrams_bk = [], [], []
    enletters_bk, enbigrams_bk, enquadrigrams_bk = [], [], []

    for ix in range(len(df)):
        item = str(df.item.iloc[ix])  # read in the column 'item'

        frstats = fr_books.get_all_meanlogstats(item, offset=1e-6)
        frletters_bk.append(frstats['letters'])
        frbigrams_bk.append(frstats['allbigrams'])
        frquadrigrams_bk.append(frstats['quadrigrams'])

        enstats = en_books.get_all_meanlogstats(item, offset=1e-6)
        enletters_bk.append(enstats['letters'])
        enbigrams_bk.append(enstats['allbigrams'])
        enquadrigrams_bk.append(enstats['quadrigrams'])

    df['frletters_bk'] = pd.Series(frletters_bk)
    df['frbigrams_bk'] = pd.Series(frbigrams_bk)
    df['frquadrigrams_bk'] = pd.Series(frquadrigrams_bk)
    df['enletters_bk'] = pd.Series(enletters_bk)
    df['enbigrams_bk'] = pd.Series(enbigrams_bk)
    df['enquadrigrams_bk'] = pd.Series(enquadrigrams_bk)

    return df


if __name__ == '__main__':
    en_books = sublexstats()
    en_books.import_csv('english-freqbooks.csv')

    fr_books = sublexstats()
    fr_books.import_csv('french-freqbooks.csv')

    for sfile in glob.glob('selected*.csv'):
        df = process(sfile, fr_books, en_books)
        outfname, ext = os.path.splitext(sfile)
        outfname += '_bk' + ext
        df.to_csv(outfname)
