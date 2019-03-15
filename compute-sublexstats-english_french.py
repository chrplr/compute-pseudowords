#! /usr/bin/env python3
# Time-stamp: <2019-03-15 14:50:45 christophe@pallier.org>

import subprocess
import string
import pandas as pd
import numpy as np
import lzma
import sublexstats

def mymin(liste):
    if liste == []:
        return np.NaN
    else:
        return np.min(liste)

def mymax(liste):
    if liste == []:
        return np.NaN
    else:
        return np.max(liste)


################# French

frdic = sublexstats.sublexstats()
frdic.import_csv('french-freqfilms.csv', caching=True)

frlex = pd.read_csv('french-freqfilms.csv', sep='\t', na_filter=False)
frfreqs = frlex.groupby('ortho').sum()

f = open("french-stats.csv", "wt")
f.write('string,frletters,frminletters,frmaxletters,frallbigrams,frminbigrams,frmaxbigrams,frquadrigrams,frminquadrigrams,frmaxquadrigrams,frwordfreq\n')

for word in frlex.ortho:
        frstats = frdic.get_all_stats(word)
        f.write('%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g\n' % (word,
                                                                            sublexstats.meanlogs(frstats['letters'], 0.000001),
                                                                            mymin(frstats['letters']),
                                                                            mymax(frstats['letters']),
                                                                            sublexstats.meanlogs(frstats['allbigrams'], 0.000001),
                                                                            mymin(frstats['allbigrams']),
                                                                            mymax(frstats['allbigrams']),
                                                                            sublexstats.meanlogs(frstats['quadrigrams'], 0.000001),
                                                                            mymin(frstats['quadrigrams']),
                                                                            mymax(frstats['quadrigrams']),
                                                                            frfreqs.freq[word]))
f.close()


################## English

endic = sublexstats.sublexstats()
endic.import_csv('english-freqfilms.csv', caching=True)

enlex = pd.read_csv('english-blp-reduced.tsv', sep='\t', na_filter=False)
enfreqs = enlex.groupby('ortho').sum()

##################

f = open("english-stats.csv", "wt")
f.write('string,enletters,enminletters,enmaxletters,enallbigrams,enminbigrams,enmaxbigrams,enquadrigrams,enminquadrigrams,enmaxquadrigrams,enwordfreq\n')

for word in enlex.ortho:
        enstats = endic.get_all_stats(word)
        f.write('%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g\n' % (word,
                                                                            sublexstats.meanlogs(enstats['letters'], 0.000001),
                                                                            mymin(enstats['letters']),
                                                                            mymax(enstats['letters']),
                                                                            sublexstats.meanlogs(enstats['allbigrams'], 0.000001),
                                                                            mymin(enstats['allbigrams']),
                                                                            mymax(enstats['allbigrams']),
                                                                            sublexstats.meanlogs(enstats['quadrigrams'], 0.000001),
                                                                            mymin(enstats['quadrigrams']),
                                                                            mymax(enstats['quadrigrams']),
                                                                            enfreqs.freq[word]))
f.close()
