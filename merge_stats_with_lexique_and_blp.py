#! /usr/bin/env python3
# Time-stamp: <2019-03-15 17:26:19 christophe@pallier.org>

import pandas as pd

lexique = pd.read_csv('French-Lexique382.csv', sep='\t')
frstats = pd.read_csv('french-stats.csv')
all = pd.merge(frstats, lexique, left_on='string', right_on='1_ortho', how='left')
all.to_csv('french-allstats.csv', index=False)


blp = pd.read_csv('British-Lexicon-Project.tsv', sep='\t')
enstats = pd.read_csv('english-stats.csv')
all = pd.merge(enstats, blp, left_on='string', right_on='spelling', how='left')
all.to_csv('english-allstats.csv', index=False)
