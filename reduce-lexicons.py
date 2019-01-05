""" Creates two reduced versions of Lexique, extracting ortho, freqfilms2 and freqlivres and two reduced version of the British Lexicon Project """


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
