# sublexical statistics for French and English #

% Time-stamp: <2019-03-15 17:03:47 christophe@pallier.org>

* `reduce-lexicons.py`: extracts lexical frequencies informations from
  `French-Lexique382.csv` and `British-Lexicon-Project.tsv` into the four files
  `english-freqbooks.csv, english-freqfilms.csv, french-freqbooks.csv,
  french-freqfilms.csv`

* `sublexstats.py`: module providing a class (sublexstats) gathering sublexical
  statistics (letter, bigram, trigram and trigram frequencies).

* `estimate-sublexstats-english-french.py`: estimates the frequencies of
  subcomponents from French and English films and books databases, and creates
  the four files `english-freqbooks.sublexstats french-freqbooks.sublexstats
  english-freqfilms.sublexstats french-freqfilms.sublexstats`

* `compute-sublexstats-english_french.py`: computes the frequencies of letters,
  bigrams, trigrams, quadrigrams in French and in English. Produces `french-stats.csv`
  `english-stats.csv`

* `compute-sublexstats-all6strings.py`: generates all possible 6-letter strings
  and computes their sublexical statistics. Outputs: `[A-Z]-strings.csv` files.

* `compute-pseudowords.py`: randomly generates 6-letter strings and computes
  their sublexical statistics.

* `add-book-stats.py`: add fields with sublexical stats to `selected*.csv` files



* super_big_stimuli_selector.py
