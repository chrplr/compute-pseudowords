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
    df_enstats, df_frstats = pd.DataFrame(), pd.DataFrame()

    for ix in range(len(df)):
        item = str(df.item.iloc[ix])  # read in the column 'item'
        frstats = fr_books.get_all_meanlogstats(item, offset=1e-6)
        enstats = en_books.get_all_meanlogstats(item, offset=1e-6)
        df_enstats = df_enstats.append(enstats, ignore_index=True)
        df_frstats = df_frstats.append(frstats, ignore_index=True)

    df_enstats = df_enstats.add_prefix('en_')
    df_frstats = df_frstats.add_prefix('fr_')
    return pd.concat([df, df_enstats, df_frstats], axis=1)




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
