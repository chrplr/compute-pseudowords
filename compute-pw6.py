#! /usr/bin/env python3
# Time-stamp: <2018-11-21 06:59:24 cp983411>


import subprocess
import string
import pandas as pd
import numpy as np
import dico

a = string.ascii_uppercase

#################
frdic = dico.dico()
frdic.import_csv('french-lexique-reduced.txt')


frlex = pd.read_csv('french-lexique-reduced.txt', sep='\t')
frlex6 = frlex.loc[frlex.ORTHO.str.len() == 6]
frfreqs = frlex6.groupby('ORTHO').sum()

##################
endic = dico.dico()
endic.import_csv('english-blp-reduced.txt')

enlex = pd.read_csv('english-blp-reduced.txt', sep='\t')
enlex6 = enlex.loc[enlex.ortho.str.len() == 6]
enfreqs = enlex6.groupby('ortho').sum()

##################


for l1 in a:
    cmd = f'xz --lzma2=dict=192MiB  -c > {l1}-string.csv.xz'
    p = subprocess.Popen(cmd,
                         shell=True, stdin=subprocess.PIPE, encoding='ascii')
    print(f'{l1} ...')
    p.stdin.write('string,frletters,frminletters,frallbigrams,frminbigrams,frquadrigrams,frminquadrigrams,frisword,frwordfreq,enletters,enminletters,enallbigrams,enminbigrams,enquadrigram,enminquadrigrams,enisword,enwordfreq\n')
    for l2 in a:
        for l3 in a:
            for l4 in a:
                for l5 in a:
                    for l6 in a:
                        w = l1 + l2 + l3 + l4 + l5 + l6
                        key = str(w.lower())
                        if key in frfreqs.index:
                            frisword = 1
                            frlexfreq = frfreqs.loc[key].freqf
                        else:
                            frisword = 0
                            frlexfreq = 0.0
                        frstats = dico.compute_stats(w, frdic)
                        if key in enfreqs.index:
                            enisword = 1
                            enlexfreq = enfreqs.loc[key].freq
                        else:
                            enisword = 0
                            enlexfreq = 0.0
                        enstats = dico.compute_stats(w, endic)
                        if np.sum(np.array(enstats['quadrigrams'] + frstats['quadrigrams'])) == 0.0:
                            None
                        #    nansquad.write()
                        else:
                            p.stdin.write('%s,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%d,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%d,%.6g\n' % (w,
                                                                                                  dico.meanlogs(frstats['letters'], 0.000001),
                                                                                                  np.min(frstats['letters']),
                                                                                                  dico.meanlogs(frstats['allbigrams'], 0.000001),
                                                                                                  np.min(frstats['allbigrams']),
                                                                                                  dico.meanlogs(frstats['quadrigrams'], 0.000001),
                                                                                                  np.min(frstats['quadrigrams']),
                                                                                                  frisword,
                                                                                                  frlexfreq,
                                                                                                  dico.meanlogs(enstats['letters'], 0.000001),
                                                                                                  np.min(enstats['letters']),
                                                                                                  dico.meanlogs(enstats['allbigrams'], 0.000001),
                                                                                                  np.min(enstats['allbigrams']),
                                                                                                  dico.meanlogs(enstats['quadrigrams'], 0.000001),
                                                                                                  np.min(enstats['quadrigrams']),
                                                                                                  enisword,
                                                                                                  enlexfreq))
    p.communicate()
