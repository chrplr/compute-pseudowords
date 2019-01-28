#! /usr/bin/env python3
# Time-stamp: <2019-01-05 13:51:19 cp983411>

""" Provides a 'sublexstats' object that tracks the frequencies of letters,
    bigrams, trigrams and words.
"""

import os.path as op
import pickle
from unidecode import unidecode
import numpy as np
import pandas as pd


EXT = 'sublexstats'  # File extension for binary files representing sublexstats objects


class sublexstats:
    def __init__(self):
        self.hashd = {}  # will contain the items and their frequencies of occurrence
        self.dico_sub = {}  # dictionnary of substitutions
        self.dico_del = {}  # dictionnary of deletions
        self.letter_distrib = {}
        self.bigram_distrib = {}
        self.openbigram_distrib = {}
        self.allbigram_distrib = {}
        self.trigram_distrib = {}
        self.quadrigram_distrib = {}

    def set_filename(self, fname):
        self.filename = fname

    def letter_distribution(self):
        return self.letter_distrib

    def bigram_distribution(self):
        return self.bigram_distrib

    def openbigram_distribution(self):
        return self.openbigram_distrib

    def allbigram_distribution(self):
        return self.allbigram_distrib

    def trigram_distribution(self):
        return self.trigram_distrib

    def quadrigram_distribution(self):
        return self.quadrigram_distrib

    def word_distribution(self):
        return self.hashd

    def normalize_weights(self):
        normalize_dictio(self.hashd)
        normalize_dictio(self.letter_distrib)
        normalize_dictio(self.bigram_distrib)
        normalize_dictio(self.openbigram_distrib)
        normalize_dictio(self.allbigram_distrib)
        normalize_dictio(self.trigram_distrib)
        normalize_dictio(self.quadrigram_distrib)

    def load(self, fname):
        with open(fname, 'rb') as f:
            tmp_dict = pickle.load(f)
        self.__dict__.clear()
        self.__dict__.update(tmp_dict)

    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self.__dict__, f, pickle.HIGHEST_PROTOCOL)

    def add(self, word, weight=1):
        """ add an item to the dictionary. """
        # if (DEBUG): print(f"adding {word} {weight}")
        addtodict(self.hashd, [word], weight)

        # add to letter, bigram and trigram counts
        addtodict(self.letter_distrib, letters(word), weight)
        addtodict(self.bigram_distrib, bigrams(word), weight)
        addtodict(self.openbigram_distrib, openbigrams(word), weight)
        addtodict(self.allbigram_distrib, allbigrams(word), weight)
        addtodict(self.trigram_distrib, trigrams(word), weight)
        addtodict(self.quadrigram_distrib, quadrigrams(word), weight)

        # create substitution patterns (bonjour -> .onjour, b.njour, bo.jour, ...)
        for i in range(len(word)):
            k = list(word)  # get the list of letters
            k[i:i+1] = '.'  # insert a '.' at position 'i'
            kk = "".join(k)
            if kk in self.dico_sub:
                if not word in self.dico_sub[kk]:
                    self.dico_sub[kk].append(word)
            else:
                self.dico_sub[kk] = [word]

        # create deletion dictionary (bonjour -> bnjour, ...)
        for i in range(len(word)):
            k = list(word)
            del k[i]
            kk = "".join(k)
            if kk in self.dico_del:
                self.dico_del[kk].append(word)
            else:
                self.dico_del[kk] = [word]

    def import_dataframe(self, df):
        """ df is a dataframe with two columns 'word' and 'weight' """
        words = df.iloc[:, 0]
        weights = df.iloc[:, 1]
        for wd, we in zip(words, weights):
            self.add(unidecode(wd), we)
        self.normalize_weights()

    def import_csv(self, filename, sep='\t', header=1, compression='infer', caching=True):
        """ Imports a csv with two columns: 'item' and 'freq'. 
            If caching=True, check if there is a file with extension EXT, and load it rather than reprocessing the csv file """
        cache_fname = modify_extension(filename, EXT)
        if caching and not(isolder(cache_fname, filename)):
            # loads the cached file
            print('Loading ' + cache_fname)
            self.load(cache_fname)
        else:
            # process the csv file
            print('Importing ' + filename + '...')
            df = pd.read_csv(filename,
                             sep=sep,
                             header=header,
                             compression=compression).dropna()
            self.import_dataframe(df)
            if (caching):
                # saves the stats in a cache file
                print('Saving ' + cache_fname)
                self.save(cache_fname)

    def import_textfile(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                for word in line.split():
                    self.add(unidecode(word))
        self.normalize_weights()

    def neighboors_substitution(self, word):
        n = []
        for i in range(len(word)):
            k = list(word)
            k[i:i+1] = '.'
            kk = "".join(k)
            if kk in self.dico_sub:
                n.extend([x for x in self.dico_sub[kk] if not x == word if not x in n])
        return n

    def neighboors_deletion(self, word):
        n = []
        for i in range(len(word)):
            k = list(word)
            del k[i]
            kk = "".join(k)
            if kk in self.hashd:
                n.append(kk)
        return n

    def neighboors_addition(self, word): # BUG: FIXME does not work
        if word in self.dico_del:
            return self.dico_del[word]
        else:
            return []

    def neighboors_transposition(self, word):
        n = []
        for i in range(len(word)-1):
            k = list(word)
            k[i], k[i+1] = k[i+1], k[i] # swap letters
            kk = "".join(k)
            if kk !=word and kk in self.hashd:
                n.append(kk)
        return n

    def get_stats_letters(self, astring):
        values = []
        for c in letters(astring):
            if c in self.letter_distrib:
                values.append(self.letter_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_stats_bigrams(self, astring):
        values = []
        for c in bigrams(astring):
            if c in self.bigram_distrib:
                values.append(self.bigram_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_stats_allbigrams(self, astring):
        values = []
        for c in allbigrams(astring):
            if c in self.allbigram_distrib:
                values.append(self.allbigram_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_stats_openbigrams(self, astring):
        values = []
        for c in openbigrams(astring):
            if c in self.openbigram_distrib:
                values.append(self.openbigram_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_stats_trigrams(self, astring):
        values = []
        for c in trigrams(astring):
            if c in self.trigram_distrib:
                values.append(self.trigram_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_stats_quadrigrams(self, astring):
        values = []
        for c in quadrigrams(astring):
            if c in self.quadrigram_distrib:
                values.append(self.quadrigram_distrib[c])
            else:
                values.append(0.0)
        return values

    def get_all_stats(self, word):
        """ extracts stats from 'self' for the subcomponents of 'word' """
        letterfreq = self.get_stats_letters(word)
        bigramfreq = self.get_stats_bigrams(word)
        openbigramfreq = self.get_stats_openbigrams(word)
        allbigramfreq = self.get_stats_allbigrams(word)
        trigramfreq = self.get_stats_trigrams(word)
        quadrigramfreq = self.get_stats_quadrigrams(word)
        return {'letters': letterfreq,
                'bigrams': bigramfreq,
                'openbigrams': openbigramfreq,
                'allbigrams': allbigramfreq,
                'trigrams': trigramfreq,
                'quadrigrams': quadrigramfreq}

    def get_all_meanlogstats(self, word, offset):
        """ extracts meanlog stats from 'self' for the subcomponents of 'word' """
        letterfreq = meanlogs(self.get_stats_letters(word), offset)
        bigramfreq = meanlogs(self.get_stats_bigrams(word), offset)
        openbigramfreq = meanlogs(self.get_stats_openbigrams(word), offset)
        allbigramfreq = meanlogs(self.get_stats_allbigrams(word), offset)
        trigramfreq = meanlogs(self.get_stats_trigrams(word), offset)
        quadrigramfreq = meanlogs(self.get_stats_quadrigrams(word), offset)
        return {'letters': letterfreq,
                'bigrams': bigramfreq,
                'openbigrams': openbigramfreq,
                'allbigrams': allbigramfreq,
                'trigrams': trigramfreq,
                'quadrigrams': quadrigramfreq}


def letters(word):
    """ Returns the list of letters in 'word'. """
    return list(word)


def bigrams(word, boundaries=False):
    """ Returns the list of bigrams in 'word'. """
    if boundaries:
        lword = '@' + word + '#'
    else:
        lword = word
    bigrams = []
    for i in range(len(lword)-1):
        bigrams.append(lword[i:i+2])
    return bigrams


def openbigrams(word, boundaries=False):
    """ Return the list of open-bigrams one letter distance in 'word'  """
    if boundaries:
        lword = '@' + word + '#'
    else:
        lword = word
    n = len(lword)
    openbig = []
    for i in range(n - 2):
        opbg = lword[i] + lword[i+2]
        openbig.append(opbg)
    return openbig


def allbigrams(word, boundaries=False):
    """ Return the list of all bigrams (open and simple) in word. """
    return bigrams(word, boundaries) + openbigrams(word, boundaries)


def trigrams(word, boundaries=False):
    if boundaries:
        lword = '@' + word + '#'
    else:
        lword = word
    trigrams = []
    for i in range(len(lword)-2):
        trigrams.append(lword[i:i+3])
    return trigrams


def quadrigrams(word, boundaries=False):
    if boundaries:
        lword = '@' + word + '#'
    else:
        lword = word
    quadrigrams = []
    for i in range(len(lword)-3):
        quadrigrams.append(lword[i:i+4])
    return quadrigrams


def addtodict(dictio, items, weight=1):
    for item in items:
        if item in dictio:
            dictio[item] += weight
        else:
            dictio[item] = weight


def normalize_dictio(dictio):
    """ Scale the values of the dictionary so that they sum to 1.
    """
    s = 0.0
    for i, w in dictio.items():
        s += w
    for i, w in dictio.items():
        dictio[i] = w / s


def meanlogs(liste, offset=1e-20):
    if np.sum(np.array(liste)) == 0.0:
        return np.NaN

    sum = 0
    for i in liste:
        sum += np.log10(i + offset)
    return sum/len(liste)


def isolder(file1, file2):
    """ Returns True if file1 is older than file2, or if file1 does not exist.
    """
    assert op.isfile(file2)
    return not(op.isfile(file1)) or (op.getmtime(file1) < op.getmtime(file2))


def modify_extension(infname, new_ext):
    basename, ext = op.splitext(infname)
    return basename + '.' + new_ext


if __name__ == '__main__':
    import pprint as pp

    frdic = sublexstats()
    frdic.import_csv('french-freqbooks.csv', caching=True)

    # two examples:
    print("bonjour : ")
    pp.pprint(frdic.get_all_meanlogstats('bonjour', offset=1e-6))
    print()
    print("aliata : ")
    pp.pprint(frdic.get_all_meanlogstats('aliata', offset=1e-6))
