% sublexical statistics
% Christophe@Pallier.org
% 


* `reduce-lexicons.py` extract lexical frequencies informations from `French-Lexique382.csv` and `British-Lexicon-Project.tsv` into the four files `english-freqbooks.csv, english-freqfilms.csv, french-freqbooks.csv, french-freqfilms.csv``


* `estimate-sublexstats-english-french.py` estimate the frequencies of subcomponents from french and english, films and books databases, and creates the four fofiles `english-freqbooks.sublexstats  french-freqbooks.sublexstats english-freqfilms.sublexstats  french-freqfilms.sublexstats`

* `compute-sublexstats-all6strings.py`  generates all possible 6-letter strings and computes their sublexical statistics. Outputs: [A-Z]-strings.csv files.

* `compute-pseudowords.py` randomly generates 6-letter strings and computes their sublexical statistics (bigram frequencies, quadrigram frequencies, ...) from lexical frequencies in English (subtlex from the British lexicaon project) and French (FreqFilms from Lexique.org).

* `add-book-stats.py`

* super_big_stimuli_selector.py
