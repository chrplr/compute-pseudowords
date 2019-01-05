#! /usr/bin/env python3
# Time-stamp: <2019-01-05 16:21:42 cp983411>


import subprocess
import string
import pandas as pd
import numpy as np
import lzma
import sublexstats

a = string.ascii_lowercase

#################
frdic = sublexstats.sublexstats()
frdic.import_csv('french-freqfilms.csv', caching=True)

frlex = pd.read_csv('french-freqfilms.csv', sep='\t')
frlex6 = frlex.loc[frlex.ortho.str.len() == 6]
frfreqs = frlex6.groupby('ortho').sum()

##################
endic = sublexstats.sublexstats()
endic.import_csv('english-freqfilms.csv', caching=True)

enlex = pd.read_csv('english-blp-reduced.tsv', sep='\t')
enlex6 = enlex.loc[enlex.ortho.str.len() == 6]
enfreqs = enlex6.groupby('ortho').sum()

##################


for l1 in a:
    print(f'{l1} ...')
    f = lzma.open(f"{l1}-strings.csv.xz", "wt")
    f.write('string,frletters,frminletters,frmaxletters,frallbigrams,frminbigrams,frmaxbigrams,frquadrigrams,frminquadrigrams,frmaxquadrigrams,frisword,frwordfreq,enletters,enminletters,enmaxletters,enallbigrams,enminbigrams,enmaxbigrams,enquadrigrams,enminquadrigrams,enmaxquadrigrams,enisword,enwordfreq\n')
    for l2 in a:
        for l3 in a:
            for l4 in a:
                for l5 in a:
                    for l6 in a:
                        w = l1 + l2 + l3 + l4 + l5 + l6
                        key = str(w)
                        if key in frfreqs.index:
                            frisword = 1
                            frlexfreq = frfreqs.loc[key].freqf
                        else:
                            frisword = 0
                            frlexfreq = 0.0
                        frstats = frdic.get_all_stats(key)
                        if key in enfreqs.index:
                            enisword = 1
                            enlexfreq = enfreqs.loc[key].freq
                        else:
                            enisword = 0
                            enlexfreq = 0.0
                        enstats = endic.get_all_stats(key)

                        if np.sum(np.array(enstats['quadrigrams'] + frstats['quadrigrams'])) == 0.0:
                            None
                        #    nansquad.write()
                        else:
                            print(key)
                            f.write('%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%d,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%d,%.6g\n' % (w,
                                                                                                  sublexstats.meanlogs(frstats['letters'], 0.000001),
                                                                                                  np.min(frstats['letters']),
                                                                                                  np.max(frstats['letters']),
                                                                                                  sublexstats.meanlogs(frstats['allbigrams'], 0.000001),
                                                                                                  np.min(frstats['allbigrams']),
                                                                                                  np.max(frstats['allbigrams']),
                                                                                                  sublexstats.meanlogs(frstats['quadrigrams'], 0.000001),
                                                                                                  np.min(frstats['quadrigrams']),
                                                                                                  np.max(frstats['quadrigrams']),
                                                                                                  frisword,
                                                                                                  frlexfreq,
                                                                                                  sublexstats.meanlogs(enstats['letters'], 0.000001),
                                                                                                  np.min(enstats['letters']),
                                                                                                  np.max(enstats['letters']),
                                                                                                  sublexstats.meanlogs(enstats['allbigrams'], 0.000001),
                                                                                                  np.min(enstats['allbigrams']),
                                                                                                  np.max(enstats['allbigrams']),
                                                                                                  sublexstats.meanlogs(enstats['quadrigrams'], 0.000001),
                                                                                                  np.min(enstats['quadrigrams']),
                                                                                                  np.max(enstats['quadrigrams']),
                                                                                                  enisword,
                                                                                                  enlexfreq))
    f.close()
