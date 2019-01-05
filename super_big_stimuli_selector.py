#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import math
from scipy import stats
import os.path as op
import os

np.set_printoptions(precision=3)

data_dir='C:\\Users\\laurent.cohen\\Dropbox (PICNIC Lab)\\manips en cours\\new_hierarchy\\giga_stats\\Vinckier-selection\\'
os.chdir(data_dir)

########################## options
select_QG=False
select_BG=False
select_LETTERS=False
select_WORDS=False
display_stats=True
nb_items=150 # per category, <200
##################################

# read nonword data
read_data = input("Voulez-vous recharger les données brutes de non mots? (o/n)")
if read_data == "o":
    a=pd.read_pickle(op.join(data_dir,'full_sublexical_nonwords_no2NaNQG_no5words_data.pkl'))
    # a=pd.read_pickle(op.join(data_dir,'full_sublexical_nonwords_no2NaNQG_data.pkl'))

# QUADRIGRAMS
if select_QG:
    # split according to QG frequency, forbidding overlapping QG frequency (ALL QG are below or above cutoff)
    cutoff=0.00001
    quad_lf_fr=(a.frmaxquadrigrams < cutoff)
    quad_hf_fr=(a.frminquadrigrams > cutoff)
    quad_lf_en=(a.enmaxquadrigrams < cutoff)
    quad_hf_en=(a.enminquadrigrams > cutoff)
    quad_lf_fr_lf_en=np.logical_and(quad_lf_fr,quad_lf_en)
    quad_lf_fr_hf_en=np.logical_and(quad_lf_fr,quad_hf_en)
    quad_hf_fr_lf_en=np.logical_and(quad_hf_fr,quad_lf_en)
    quad_hf_fr_hf_en=np.logical_and(quad_hf_fr,quad_hf_en)
    
    print("quad_lf_fr_lf_en", sum(quad_lf_fr_lf_en==1))
    print("quad_lf_fr_hf_en", sum(quad_lf_fr_hf_en==1))
    print("quad_hf_fr_lf_en", sum(quad_hf_fr_lf_en==1))
    print("quad_hf_fr_hf_en", sum(quad_hf_fr_hf_en==1))
    
    C1 = a[quad_hf_fr_hf_en]
    C2 = a[quad_hf_fr_lf_en]
    C3 = a[quad_lf_fr_hf_en]
    C4 = a[quad_lf_fr_lf_en]
        
    fbimin= -3.5
    fbimax= -2
    C1sub = C1.loc[np.logical_and(np.logical_and(C1.frbigrams > fbimin, C1.frbigrams < fbimax), np.logical_and(C1.enbigrams > fbimin, C1.enbigrams < fbimax))]
    C1sub = C1sub.copy()
    C2sub = C2.loc[np.logical_and(np.logical_and(C2.frbigrams > fbimin, C2.frbigrams < fbimax), np.logical_and(C2.enbigrams > fbimin, C2.enbigrams < fbimax))]
    C2sub = C2sub.copy()
    C3sub = C3.loc[np.logical_and(np.logical_and(C3.frbigrams > fbimin, C3.frbigrams < fbimax), np.logical_and(C3.enbigrams > fbimin, C3.enbigrams < fbimax))]
    C3sub = C3sub.copy()
    C4sub = C4.loc[np.logical_and(np.logical_and(C4.frbigrams > fbimin+.3, C4.frbigrams < fbimax-0.3), np.logical_and(C4.enbigrams > fbimin+.3, C4.enbigrams < fbimax-0.3))]
    C4sub = C4sub.copy()
    
    sns.distplot(C1sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C2sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C3sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C4sub.frbigrams, bins=30, kde=False, norm_hist=True);
    
    print(len(C1sub),len(C2sub),len(C3sub),len(C4sub))
    nmin = min ([len(C1sub), len(C2sub), len(C3sub), len(C4sub)])
    print(nmin)
    C1sub = C1sub.sample(nmin)
    C2sub = C2sub.sample(nmin)
    C3sub = C3sub.sample(nmin)
    C4sub = C4sub.sample(nmin)
    
    C1sub['distbi'] = np.abs(C1sub.frbigrams + 2.6)**2 + np.abs(C1sub.enbigrams + 2.6)**2
    C2sub['distbi'] = np.abs(C2sub.frbigrams + 2.6)**2 + np.abs(C2sub.enbigrams + 2.6)**2
    C3sub['distbi'] = np.abs(C3sub.frbigrams + 2.6)**2 + np.abs(C3sub.enbigrams + 2.6)**2
    C4sub['distbi'] = np.abs(C4sub.frbigrams + 2.6)**2 + np.abs(C4sub.enbigrams + 2.6)**2
    
    N = nb_items
    selected_C1 = C1sub.sort_values('distbi').head(N)
    selected_C2 = C2sub.sort_values('distbi').head(N)
    selected_C3 = C3sub.sort_values('distbi').head(N)
    selected_C4 = C4sub.sort_values('distbi').head(N)
    
    selected_C1.to_csv("selected_quad_hf_fr_hf_en.csv", index=False)
    selected_C2.to_csv("selected_quad_hf_fr_lf_en.csv", index=False)
    selected_C3.to_csv("selected_quad_lf_fr_hf_en.csv", index=False)
    selected_C4.to_csv("selected_quad_lf_fr_lf_en.csv", index=False)
    
# BIGRAMS
if select_BG:

    # try to identify subsets with different mean BG freq X languages
    # increasing the distance between the means
    bg_cutoff_h=-3.13 + 0.4
    bg_cutoff_l=-3.13 - 0.4
    bg_lf_fr=(a.frbigrams < bg_cutoff_l)
    bg_hf_fr=(a.frbigrams > bg_cutoff_h)
    bg_lf_en=(a.enbigrams < bg_cutoff_l)
    bg_hf_en=(a.enbigrams > bg_cutoff_h)
    bg_lf_fr_lf_en=np.logical_and(bg_lf_fr,bg_lf_en)
    bg_lf_fr_hf_en=np.logical_and(bg_lf_fr,bg_hf_en)
    bg_hf_fr_lf_en=np.logical_and(bg_hf_fr,bg_lf_en)
    bg_hf_fr_hf_en=np.logical_and(bg_hf_fr,bg_hf_en)
    
    print("bg_lf_fr_lf_en", sum(bg_lf_fr_lf_en==1))
    print("bg_lf_fr_hf_en", sum(bg_lf_fr_hf_en==1))
    print("bg_hf_fr_lf_en", sum(bg_hf_fr_lf_en==1))
    print("bg_hf_fr_hf_en", sum(bg_hf_fr_hf_en==1))
    
    C1 = a[bg_hf_fr_hf_en]
    C2 = a[bg_hf_fr_lf_en]
    C3 = a[bg_lf_fr_hf_en]
    C4 = a[bg_lf_fr_lf_en]
    
    flettrersmin= -1.6 # -1.6
    flettrersmax= -1.4 # -1.4
    C1sub = C1.loc[np.logical_and(np.logical_and(C1.frletters > flettrersmin, C1.frletters < flettrersmax), np.logical_and(C1.enletters > flettrersmin, C1.enletters < flettrersmax))]
    C1sub = C1sub.copy()
    C2sub = C2.loc[np.logical_and(np.logical_and(C2.frletters > flettrersmin, C2.frletters < flettrersmax), np.logical_and(C2.enletters > flettrersmin, C2.enletters < flettrersmax))]
    C2sub = C2sub.copy()
    C3sub = C3.loc[np.logical_and(np.logical_and(C3.frletters > flettrersmin, C3.frletters < flettrersmax), np.logical_and(C3.enletters > flettrersmin, C3.enletters < flettrersmax))]
    C3sub = C3sub.copy()
    C4sub = C4.loc[np.logical_and(np.logical_and(C4.frletters > flettrersmin, C4.frletters < flettrersmax), np.logical_and(C4.enletters > flettrersmin, C4.enletters < flettrersmax))]
    C4sub = C4sub.copy()
    
    sns.distplot(C1sub.frletters, bins=30, kde=False, norm_hist=True);
    sns.distplot(C2sub.frletters, bins=30, kde=False, norm_hist=True);
    sns.distplot(C3sub.frletters, bins=30, kde=False, norm_hist=True);
    sns.distplot(C4sub.frletters, bins=30, kde=False, norm_hist=True);
        
    print(len(C1sub),len(C2sub),len(C3sub),len(C4sub))
    nmin = min ([len(C1sub), len(C2sub), len(C3sub), len(C4sub)])
    C1sub = C1sub.sample(nmin)
    C2sub = C2sub.sample(nmin)
    C3sub = C3sub.sample(nmin)
    C4sub = C4sub.sample(nmin)
    
    target_mean = 1.5
    C1sub['distlett'] = np.abs(C1sub.frletters + target_mean)**2 + np.abs(C1sub.enletters + target_mean)**2
    C2sub['distlett'] = np.abs(C2sub.frletters + target_mean)**2 + np.abs(C2sub.enletters + target_mean)**2
    C3sub['distlett'] = np.abs(C3sub.frletters + target_mean)**2 + np.abs(C3sub.enletters + target_mean)**2
    C4sub['distlett'] = np.abs(C4sub.frletters + target_mean)**2 + np.abs(C4sub.enletters + target_mean)**2
    
    N = 200
    selected_C1 = C1sub.sort_values('distlett').head(N)
    selected_C2 = C2sub.sort_values('distlett').head(N)
    selected_C3 = C3sub.sort_values('distlett').head(N)
    selected_C4 = C4sub.sort_values('distlett').head(N)
    
    target_mean = 6 
    selected_C1['distquad'] = np.abs(selected_C1.frquadrigrams + target_mean)**2 + np.abs(selected_C1.enquadrigrams + target_mean)**2
    selected_C2['distquad'] = np.abs(selected_C2.frquadrigrams + target_mean)**2 + np.abs(selected_C2.enquadrigrams + target_mean)**2
    selected_C3['distquad'] = np.abs(selected_C3.frquadrigrams + target_mean)**2 + np.abs(selected_C3.enquadrigrams + target_mean)**2
    selected_C4['distquad'] = np.abs(selected_C4.frquadrigrams + target_mean)**2 + np.abs(selected_C4.enquadrigrams + target_mean)**2
    
    N = nb_items
    selected_C1 = selected_C1.sort_values('distquad').head(N)
    selected_C2 = selected_C2.sort_values('distquad').head(N)
    selected_C3 = selected_C3.sort_values('distquad').head(N)
    selected_C4 = selected_C4.sort_values('distquad').head(N)
    
    selected_C1.to_csv("selected_bg_hf_fr_hf_en.csv", index=False)
    selected_C2.to_csv("selected_bg_hf_fr_lf_en.csv", index=False)
    selected_C3.to_csv("selected_bg_lf_fr_hf_en.csv", index=False)
    selected_C4.to_csv("selected_bg_lf_fr_lf_en.csv", index=False)
    
# LETTERS
if select_LETTERS:

    # try to identify subsets with different mean let freq X languages
    # increasing the distance between the means
    let_cutoff_h=-1.5 + 0.18
    let_cutoff_l=-1.5 - 0.18
    
    let_cutoff_h=-1.59 + 0.22
    let_cutoff_l=-1.59 - 0.22
    
    let_lf_fr=(a.frletters < let_cutoff_l)
    let_hf_fr=(a.frletters > let_cutoff_h)
    let_lf_en=(a.enletters < let_cutoff_l)
    let_hf_en=(a.enletters > let_cutoff_h)
    let_lf_fr_lf_en=np.logical_and(let_lf_fr,let_lf_en)
    let_lf_fr_hf_en=np.logical_and(let_lf_fr,let_hf_en)
    let_hf_fr_lf_en=np.logical_and(let_hf_fr,let_lf_en)
    let_hf_fr_hf_en=np.logical_and(let_hf_fr,let_hf_en)
    
    print("let_lf_fr_lf_en", sum(let_lf_fr_lf_en==1))
    print("let_lf_fr_hf_en", sum(let_lf_fr_hf_en==1))
    print("let_hf_fr_lf_en", sum(let_hf_fr_lf_en==1))
    print("let_hf_fr_hf_en", sum(let_hf_fr_hf_en==1))
    
    
    # restrict to lf bg then
    # try to identify subsets with different mean let freq X languages
    # increasing the distance between the means
    bg_cutoff=-4.5
    
    let_cutoff_h=-2.1 + 0.2
    let_cutoff_l=-2.1 - 0.2
    
    let_lf_fr=np.logical_and((a.frletters < let_cutoff_l),np.logical_and(a.frbigrams < bg_cutoff,a.enbigrams < bg_cutoff))
    let_hf_fr=np.logical_and((a.frletters > let_cutoff_h),np.logical_and(a.frbigrams < bg_cutoff,a.enbigrams < bg_cutoff))
    let_lf_en=np.logical_and((a.enletters < let_cutoff_l),np.logical_and(a.frbigrams < bg_cutoff,a.enbigrams < bg_cutoff))
    let_hf_en=np.logical_and((a.enletters > let_cutoff_h),np.logical_and(a.frbigrams < bg_cutoff,a.enbigrams < bg_cutoff))
    let_lf_fr_lf_en=np.logical_and(let_lf_fr,let_lf_en)
    let_lf_fr_hf_en=np.logical_and(let_lf_fr,let_hf_en)
    let_hf_fr_lf_en=np.logical_and(let_hf_fr,let_lf_en)
    let_hf_fr_hf_en=np.logical_and(let_hf_fr,let_hf_en)
    
    print("let_lf_fr_lf_en", sum(let_lf_fr_lf_en==1))
    print("let_lf_fr_hf_en", sum(let_lf_fr_hf_en==1))
    print("let_hf_fr_lf_en", sum(let_hf_fr_lf_en==1))
    print("let_hf_fr_hf_en", sum(let_hf_fr_hf_en==1))
        
    C1 = a[let_hf_fr_hf_en]
    C2 = a[let_hf_fr_lf_en]
    C3 = a[let_lf_fr_hf_en]
    C4 = a[let_lf_fr_lf_en]
    
    len(C1), len(C2), len(C3), len(C4)
    
    fbigramsmin= -4.97 
    fbigramsmax= -4.63 
    C1sub = C1.loc[np.logical_and(np.logical_and(C1.frbigrams > fbigramsmin, C1.frbigrams < fbigramsmax), np.logical_and(C1.enbigrams > fbigramsmin, C1.enbigrams < fbigramsmax))]
    C1sub = C1sub.copy()
    C2sub = C2.loc[np.logical_and(np.logical_and(C2.frbigrams > fbigramsmin, C2.frbigrams < fbigramsmax), np.logical_and(C2.enbigrams > fbigramsmin, C2.enbigrams < fbigramsmax))]
    C2sub = C2sub.copy()
    C3sub = C3.loc[np.logical_and(np.logical_and(C3.frbigrams > fbigramsmin, C3.frbigrams < fbigramsmax), np.logical_and(C3.enbigrams > fbigramsmin, C3.enbigrams < fbigramsmax))]
    C3sub = C3sub.copy()
    C4sub = C4.loc[np.logical_and(np.logical_and(C4.frbigrams > fbigramsmin, C4.frbigrams < fbigramsmax), np.logical_and(C4.enbigrams > fbigramsmin, C4.enbigrams < fbigramsmax))]
    C4sub = C4sub.copy()
    
    sns.distplot(C1sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C2sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C3sub.frbigrams, bins=30, kde=False, norm_hist=True);
    sns.distplot(C4sub.frbigrams, bins=30, kde=False, norm_hist=True);
    
    nmin = min ([len(C1sub), len(C2sub), len(C3sub), len(C4sub)])
    C1sub = C1sub.sample(nmin)
    C2sub = C2sub.sample(nmin)
    C3sub = C3sub.sample(nmin)
    C4sub = C4sub.sample(nmin)
       
    target_mean = 4.8 # put the positive value
    C1sub['distbi'] = np.abs(C1sub.frbigrams + target_mean)**2 + np.abs(C1sub.enbigrams + target_mean)**2
    C2sub['distbi'] = np.abs(C2sub.frbigrams + target_mean)**2 + np.abs(C2sub.enbigrams + target_mean)**2
    C3sub['distbi'] = np.abs(C3sub.frbigrams + target_mean)**2 + np.abs(C3sub.enbigrams + target_mean)**2
    C4sub['distbi'] = np.abs(C4sub.frbigrams + target_mean)**2 + np.abs(C4sub.enbigrams + target_mean)**2
    
    N = nb_items
    selected_C1 = C1sub.sort_values('distbi').head(N)
    selected_C2 = C2sub.sort_values('distbi').head(N)
    selected_C3 = C3sub.sort_values('distbi').head(N)
    selected_C4 = C4sub.sort_values('distbi').head(N)
    
    selected_C1.to_csv("selected_let_hf_fr_hf_en.csv", index=False)
    selected_C2.to_csv("selected_let_hf_fr_lf_en.csv", index=False)
    selected_C3.to_csv("selected_let_lf_fr_hf_en.csv", index=False)
    selected_C4.to_csv("selected_let_lf_fr_lf_en.csv", index=False)
    
# WORDS 
if select_WORDS:
    
    a=pd.read_pickle(op.join(data_dir,'full_sublexical_realwords_data.pkl'))

    # split according to QG frequency, forbidding overlapping QG frequency (ALL QG are below or above cutoff)
    cutoff=0.00001
    quad_lf_fr=(a.frmaxquadrigrams < cutoff)
    quad_hf_fr=(a.frminquadrigrams > cutoff)
    quad_lf_en=(a.enmaxquadrigrams < cutoff)
    quad_hf_en=(a.enminquadrigrams > cutoff)
    quad_lf_fr_lf_en=np.logical_and(quad_lf_fr,quad_lf_en)
    quad_lf_fr_hf_en=np.logical_and(quad_lf_fr,quad_hf_en)
    quad_hf_fr_lf_en=np.logical_and(quad_hf_fr,quad_lf_en)
    quad_hf_fr_hf_en=np.logical_and(quad_hf_fr,quad_hf_en)
    
    print("quad_lf_fr_lf_en", sum(quad_lf_fr_lf_en==1))
    print("quad_lf_fr_hf_en", sum(quad_lf_fr_hf_en==1))
    print("quad_hf_fr_lf_en", sum(quad_hf_fr_lf_en==1))
    print("quad_hf_fr_hf_en", sum(quad_hf_fr_hf_en==1))
       
    C1 = a[quad_hf_fr_hf_en]
    
    fbimin= -3.5
    fbimax= -2
    C1sub = C1.loc[np.logical_and(np.logical_and(C1.frbigrams > fbimin, C1.frbigrams < fbimax), np.logical_and(C1.enbigrams > fbimin, C1.enbigrams < fbimax))]
    C1sub = C1sub.copy()
    
    sns.distplot(C1sub.frbigrams, bins=30, kde=False, norm_hist=True);
    
    C1sub_HFL=C1sub.loc[np.logical_or(C1sub.frwordfreq>1,C1sub.enwordfreq>10)]
    
    print(len(C1sub_HFL))
    C1sub_HFL = C1sub_HFL.copy()
    
    C1sub_HFL['distbi_en'] = np.abs(C1sub_HFL.enbigrams + 2.6)**2
    C1sub_HFL['distbi_fr'] = np.abs(C1sub_HFL.frbigrams + 2.6)**2
    
    N = nb_items
    selected_C1_en = C1sub_HFL[np.logical_and(C1sub_HFL.enisword == True,C1sub_HFL.frisword == False)].sort_values('distbi_en').head(N)
    selected_C1_fr = C1sub_HFL[np.logical_and(C1sub_HFL.enisword == False,C1sub_HFL.frisword == True)].sort_values('distbi_fr').head(N)
    
    selected_C1_en.to_csv("selected_en_words.csv", index=False)
    selected_C1_fr.to_csv("selected_fr_words.csv", index=False)

# DISPLAY SELECTED
if display_stats:
    
    en_words=pd.read_csv(op.join(data_dir,'selected_en_words.csv'))
    fr_words=pd.read_csv(op.join(data_dir,'selected_fr_words.csv'))
    
    quad_hf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_quad_hf_fr_hf_en.csv'))
    quad_hf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_quad_hf_fr_lf_en.csv'))
    quad_lf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_quad_lf_fr_hf_en.csv'))
    quad_lf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_quad_lf_fr_lf_en.csv'))
    
    bg_hf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_bg_hf_fr_hf_en.csv'))
    bg_hf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_bg_hf_fr_lf_en.csv'))
    bg_lf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_bg_lf_fr_hf_en.csv'))
    bg_lf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_bg_lf_fr_lf_en.csv'))
    
    let_hf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_let_hf_fr_hf_en.csv'))
    let_hf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_let_hf_fr_lf_en.csv'))
    let_lf_fr_hf_en=pd.read_csv(op.join(data_dir,'selected_let_lf_fr_hf_en.csv'))
    let_lf_fr_lf_en=pd.read_csv(op.join(data_dir,'selected_let_lf_fr_lf_en.csv'))
    
    
    rows=["QG experiment","BG experiment","LET experiment","real WORDS"]
    
    fs = 14
    
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(13, 15), sharey=False)
    
    r=0
    
    labels = ['fhh','fhl','flh','fll','ehh','ehl','elh','ell']
    
    data =  [quad_hf_fr_hf_en.frquadrigrams,
            quad_hf_fr_lf_en.frquadrigrams,
            quad_lf_fr_hf_en.frquadrigrams,
            quad_lf_fr_lf_en.frquadrigrams,
            quad_hf_fr_hf_en.enquadrigrams,
            quad_hf_fr_lf_en.enquadrigrams,
            quad_lf_fr_hf_en.enquadrigrams,
            quad_lf_fr_lf_en.enquadrigrams]
    
    axes[r, 0].boxplot(data, labels=labels)
    axes[r, 0].set_ylim([-6.5,-2.5])
    axes[r, 0].set_title('QG frequency', fontsize=fs)
    
    data =  [quad_hf_fr_hf_en.frbigrams,
            quad_hf_fr_lf_en.frbigrams,
            quad_lf_fr_hf_en.frbigrams,
            quad_lf_fr_lf_en.frbigrams,
            quad_hf_fr_hf_en.enbigrams,
            quad_hf_fr_lf_en.enbigrams,
            quad_lf_fr_hf_en.enbigrams,
            quad_lf_fr_lf_en.enbigrams]
    
    axes[r, 1].boxplot(data, labels=labels)
    axes[r, 1].set_ylim([-5,-2])
    axes[r, 1].set_title('BG frequency', fontsize=fs)
    
    data =  [quad_hf_fr_hf_en.frletters,
            quad_hf_fr_lf_en.frletters,
            quad_lf_fr_hf_en.frletters,
            quad_lf_fr_lf_en.frletters,
            quad_hf_fr_hf_en.enletters,
            quad_hf_fr_lf_en.enletters,
            quad_lf_fr_hf_en.enletters,
            quad_lf_fr_lf_en.enletters]
    
    axes[r, 2].boxplot(data, labels=labels)
    axes[r, 2].set_ylim([-3,-1])
    axes[r, 2].set_title('LET frequency', fontsize=fs)
    
    r=r+1
    
    data =  [bg_hf_fr_hf_en.frquadrigrams,
            bg_hf_fr_lf_en.frquadrigrams,
            bg_lf_fr_hf_en.frquadrigrams,
            bg_lf_fr_lf_en.frquadrigrams,
            bg_hf_fr_hf_en.enquadrigrams,
            bg_hf_fr_lf_en.enquadrigrams,
            bg_lf_fr_hf_en.enquadrigrams,
            bg_lf_fr_lf_en.enquadrigrams]
    
    axes[r, 0].boxplot(data, labels=labels)
    axes[r, 0].set_ylim([-6.5,-2.5])
    axes[r, 0].set_title('QG frequency', fontsize=fs)
    
    data =  [bg_hf_fr_hf_en.frbigrams,
            bg_hf_fr_lf_en.frbigrams,
            bg_lf_fr_hf_en.frbigrams,
            bg_lf_fr_lf_en.frbigrams,
            bg_hf_fr_hf_en.enbigrams,
            bg_hf_fr_lf_en.enbigrams,
            bg_lf_fr_hf_en.enbigrams,
            bg_lf_fr_lf_en.enbigrams]
    
    axes[r, 1].boxplot(data, labels=labels)
    axes[r, 1].set_ylim([-5,-2])
    axes[r, 1].set_title('BG frequency', fontsize=fs)
    
    data =  [bg_hf_fr_hf_en.frletters,
            bg_hf_fr_lf_en.frletters,
            bg_lf_fr_hf_en.frletters,
            bg_lf_fr_lf_en.frletters,
            bg_hf_fr_hf_en.enletters,
            bg_hf_fr_lf_en.enletters,
            bg_lf_fr_hf_en.enletters,
            bg_lf_fr_lf_en.enletters]
    
    axes[r, 2].boxplot(data, labels=labels)
    axes[r, 2].set_ylim([-3,-1])
    axes[r, 2].set_title('LET frequency', fontsize=fs)
    
    data =  [let_hf_fr_hf_en.frquadrigrams,
            let_hf_fr_lf_en.frquadrigrams,
            let_lf_fr_hf_en.frquadrigrams,
            let_lf_fr_lf_en.frquadrigrams,
            let_hf_fr_hf_en.enquadrigrams,
            let_hf_fr_lf_en.enquadrigrams,
            let_lf_fr_hf_en.enquadrigrams,
            let_lf_fr_lf_en.enquadrigrams]
    
    r=r+1
    
    axes[r, 0].boxplot(data, labels=labels)
    axes[r, 0].set_ylim([-6.5,-2.5])
    axes[r, 0].set_title('QG frequency', fontsize=fs)
    
    data =  [let_hf_fr_hf_en.frbigrams,
            let_hf_fr_lf_en.frbigrams,
            let_lf_fr_hf_en.frbigrams,
            let_lf_fr_lf_en.frbigrams,
            let_hf_fr_hf_en.enbigrams,
            let_hf_fr_lf_en.enbigrams,
            let_lf_fr_hf_en.enbigrams,
            let_lf_fr_lf_en.enbigrams]
    
    axes[r, 1].boxplot(data, labels=labels)
    axes[r, 1].set_ylim([-5,-2])
    axes[r, 1].set_title('BG frequency', fontsize=fs)
    
    data =  [let_hf_fr_hf_en.frletters,
            let_hf_fr_lf_en.frletters,
            let_lf_fr_hf_en.frletters,
            let_lf_fr_lf_en.frletters,
            let_hf_fr_hf_en.enletters,
            let_hf_fr_lf_en.enletters,
            let_lf_fr_hf_en.enletters,
            let_lf_fr_lf_en.enletters]
    
    axes[r, 2].boxplot(data, labels=labels)
    axes[r, 2].set_ylim([-3,-1])
    axes[r, 2].set_title('LET frequency', fontsize=fs)
    
    labels = ['f_hh','f_fw','f_ew','','e_hh','e_fw','e_ew','']
    
    data =  [quad_hf_fr_hf_en.frquadrigrams,
            en_words.frquadrigrams,
            fr_words.frquadrigrams,
            [],
            quad_hf_fr_hf_en.enquadrigrams,
            en_words.enquadrigrams,
            fr_words.enquadrigrams,
            []]
    
    r=r+1
    
    axes[r, 0].boxplot(data, labels=labels)
    axes[r, 0].set_ylim([-6.5,-2.5])
    axes[r, 0].set_title('QG frequency', fontsize=fs)
    
    data =  [quad_hf_fr_hf_en.frbigrams,
            en_words.frbigrams,
            fr_words.frbigrams,
            [],
            quad_hf_fr_hf_en.enbigrams,
            en_words.enbigrams,
            fr_words.enbigrams,
            []]
    
    axes[r, 1].boxplot(data, labels=labels)
    axes[r, 1].set_ylim([-5,-2])
    axes[r, 1].set_title('BG frequency', fontsize=fs)
    
    data =  [quad_hf_fr_hf_en.frletters,
            en_words.frletters,
            fr_words.frletters,
            [],
            quad_hf_fr_hf_en.enletters,
            en_words.enletters,
            fr_words.enletters,
            []]
    
    axes[r, 2].boxplot(data, labels=labels)
    axes[r, 2].set_ylim([-3,-1])
    axes[r, 2].set_title('LET frequency', fontsize=fs)
    
    for ax, row in zip(axes[:,0], rows):
        ax.set_ylabel(row, rotation=90, fontsize=14)
        
    fig.subplots_adjust(hspace = 0.4)
    fig.subplots_adjust(wspace = 0.35)
    plt.show()
    fig.savefig("stats_selected_items.jpg")
    
