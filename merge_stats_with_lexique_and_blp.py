#! /usr/bin/env python3
# Time-stamp: <2019-04-01 20:31:05 christophe@pallier.org>

import pandas as pd

lexique = pd.read_csv('French-Lexique382.csv', sep='\t')
frstats = pd.read_csv('french-stats.csv')
all = pd.concat([frstats, lexique], axis=1)
all.to_csv('french-allstats.csv', index=False)


blp = pd.read_csv('British-Lexicon-Project.tsv', sep='\t')
enstats = pd.read_csv('english-stats.csv')
all = pd.concat([enstats, blp], axis=1)
all.to_csv('english-allstats.csv', index=False)
