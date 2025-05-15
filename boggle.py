# List from https://github.com/chrplr/openlexicon/tree/master/datasets-info/Liste-de-mots-francais-Gutenberg

import sys
import unicodedata

words = dict()
result = set()
grid = ''
min_length = 3
dict_file = "liste.de.mots.francais.frgut.txt"
neighbors = [(1, 5, 4), (0, 2, 6, 5, 4), (1, 3, 7, 6, 5), (2, 7, 6), 
             (0, 1, 5, 9, 8), (0, 1, 2, 6, 10, 9, 8, 4), (1, 2, 3, 7, 11, 10, 9, 5), (2, 3, 11, 10, 6),
             (4, 5, 9, 13, 12), (4, 5, 6, 10, 14, 13, 12, 8), (5, 6, 7, 11, 15, 14, 13, 9), (6, 7, 15, 14, 10),
             (8, 9, 13), (8, 9, 10, 14, 12), (9, 10, 11, 15, 13), (10, 11, 14)]


def is_prefix(word: str, dico: dict) -> bool:
    """ Tell if a word is a prefix of known words """
    if len(word) == 0:
        return dico
    elif len(word) >= 1 and word[0] not in dico:
        return dict()
    else:
        return is_prefix(word[1:], dico[word[0]])


def put_in_dictionary(word: str, dico: dict) -> None:
    """ Add a word in our optimized dictionary """
    if len(word) == 0:
        dico['.'] = '.'
        return
    elif len(word) >= 1 and word[0] not in dico:
        dico[word[0]] = dict()
    
    put_in_dictionary(word[1:], dico[word[0]])


def solve(prefix: str, indexes: list) -> None:
    """ Recursive solver """
    dico = is_prefix(prefix, words)
    if len(dico) > 0:
        # This is a valid prefix, continue exploring
        if '.' in dico and len(prefix) >= min_length:
            # A prefix can be a valid word
            result.add(prefix)
        # Now explore all neighboring cells if not already done
        for neighbor in neighbors[indexes[-1]]:
            if neighbor not in indexes:
                # Duplicates are not allowed
                solve(prefix + grid[neighbor], indexes + [neighbor])


if __name__ == "__main__":
    # Get arguments from command-line
    grid = sys.argv[1].upper()
    if len(sys.argv) > 2:
        dict_file = sys.argv[2]
    if len(sys.argv) > 3:
        min_length = int(sys.argv[3])
    
    print("Read dictionary")
    with open(dict_file, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.rstrip()
            if '-' in line:
                # No compound words in boggle
                continue
            word = ''.join(c for c in unicodedata.normalize('NFKD', line) if not unicodedata.combining(c)).upper()
            put_in_dictionary(word, words)
    
    print("Solve puzzle")
    
    for i in range(16):
        # Each cell is a valid starting point
        solve(grid[i], [i])
    
    print(len(result))
    for word in sorted(result, key=lambda s: len(s), reverse=True):
        print(word)
