#! /usr/bin/env python3
# Time-stamp: <2019-03-15 14:37:01 christophe@pallier.org>

"""
Creates reduced versions of Lexique and the British Lexicon Project:

    french-freqfilms.csv
    french-freqbooks.csv
    english-freqfilms.csv
    english-freqbooks.csv

"""

import pandas as pd

## French 
fr = pd.read_csv('French-Lexique382.csv', sep='\t')

fr[['1_ortho', '9_freqfilms2']].rename(columns={'1_ortho': 'ortho',
                                               '9_freqfilms2':'freq'}).to_csv('french-freqfilms.csv', sep='\t', index=False)

fr[['1_ortho', '10_freqlivres']].rename(columns={'1_ortho': 'ortho',
                                                '10_freqlivres': 'freq'}).to_csv('french-freqbooks.csv', sep='\t', index=False)

# English

en = pd.read_csv('British-Lexicon-Project.tsv', sep='\t')

en[['spelling', 'bnc.frequency.million']].rename(columns={'spelling': 'ortho',
                                                           'subtlex.frequency': 'freq'}).to_csv('english-freqfilms.csv', sep='\t', index=False)

en[['spelling', 'bnc.frequency.million']].rename(columns={'spelling': 'ortho',
                                                           'bnc.frequency.million': 'freq'}).to_csv('english-freqbooks.csv', sep='\t', index=False)
