'''
teach_peace.py

Summary: Code for finding word pairs in a given dictionary
that satisfy the "teach-peace" properpty.

Author: David Abel, david-abel.github.io
Date: April 2019
'''

# Python imports.
import random
import operator
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot

def _remove_non_alpha(line):
    '''
    Args;
        line (str)

    Returns:
        (str)

    Summary:
        Removes all non-alpha symbols and replaces them with spaces.
    '''
    line = line.lower()
    line = line.strip()
    bad_symbols = ["\n", "\t", ",", ".", "-", "!", "?", "'", ":", "-", "_", "[", "]", '"', '`', '(', ')', ';']
        
    for sym in bad_symbols:
        line = line.replace(sym, " ")

    return line

def convert_to_corpus(file_name, out_file_name):
    '''
    Args:
        file_name (str)
        out_file_name (str)

    Summary:
        Takes a given txt file and turns it into a file that
        contains all unique words in @file_name, one word per line.
    '''

    # Get unique words in text.
    word_dict = defaultdict(int)
    for line in file(file_name, "r").readlines():
        line = _remove_non_alpha(line)
        line = line.split(" ")
        for word in line:
            if _is_bad_word(word):
                continue
            # out_file.write(word + "\n")
            word_dict[word] += 1

    sorted_words = sorted(word_dict.keys())

    # Write all words to out file.
    out_file = file(out_file_name, "w+")
    for word in sorted_words:
        out_file.write(word + "\n")
    out_file.close()

def load_words_to_dict(file_name="words.txt"):
    '''
    Returns:
        (defaultdict(int)): Loads all words in @file_name into a word dict with:
            Key-->word
            Val-->1
    '''
    word_dict = defaultdict(int)
    for word in file(file_name, "r").readlines():
        word_dict[word.strip().lower()] = 1
    return word_dict

def get_words_by_len_dict(all_words):
    '''
    Args:
        all_words (list)
    '''
    words_by_len = defaultdict(set)
    for w in all_words:
        words_by_len[len(w)].add(w)
    
    return words_by_len

def is_teach_peace_property(word_one, word_two, req_middle_match_len=2):
    '''
    Args:
        word_one (str)
        word_two (str)
        req_middle_match_len (int)

    Returns:
        (bool)
    '''
    if word_one == word_two:
        return False

    for i in range(1, len(word_one)):
        for j in range(1, len(word_two)):
            if len(word_one[i:-i]) >= req_middle_match_len and word_one[i:-i] == word_two[j:-j] and word_one[:i] != word_two[:j] and word_one[-i:] != word_two[-j:]:
                return True

    return False

def get_all_teach_peace_word_pairs(words_by_len_dict, req_middle_match_len=2):
    '''
    Args:
        word_dict (dict)
        req_middle_match_len (int)

    Returns:
        (dict)
    '''
    all_tp_words = defaultdict(set)
    for word_length in words_by_len_dict.keys():
        if word_length < req_middle_match_len:
            # Words aren't long enough yet.
            continue

        for word_one in words_by_len_dict[word_length]:
            for word_two in words_by_len_dict[word_length]:
                if is_teach_peace_property(word_one, word_two, req_middle_match_len=req_middle_match_len):
                    all_tp_words[word_one].add(word_two)
                    all_tp_words[word_two].add(word_one)

    return all_tp_words

def display_results(tp_words, req_middle_match_len=2):
    '''
    Args:
        tp_words (dict)
        req_middle_match_len (int)
    '''

    for word in tp_words:
      print "\t", word, tp_words[word]

    longest_word_indices = [len(tp_words.keys()[i]) for i in range(len(tp_words.keys()))]
    max_length = max(longest_word_indices)
    index = longest_word_indices.index(max_length)
    longest_word = tp_words.keys()[index]

    total_pairings = len(tp_words.keys())
    print "\tTotal pairings:", total_pairings

    return total_pairings


def main():

    # Data structs.
    total_pairings = defaultdict(int)
    x_axis = range(1, 8)
    y_axis = [0]*len(x_axis)
    plot = False

    # Main experiment.
    for req_middle_match_len in x_axis:
        print "Running for", req_middle_match_len, "matches."

        # Load words.
        all_words = load_words_to_dict(file_name="common_words.txt")

        words_by_len = get_words_by_len_dict(all_words)

        # Get all TP words.
        all_tp_words = get_all_teach_peace_word_pairs(words_by_len, req_middle_match_len=req_middle_match_len)

        if len(all_tp_words.keys()) > 0:
            # Show results.
            y_axis[req_middle_match_len - 1] = display_results(all_tp_words, req_middle_match_len=req_middle_match_len)
        else:
            y_axis[req_middle_match_len - 1] = 0

    if plot:
        # Plot
        y_label = "Teach Peace Property Prevalance"

        pyplot.xlabel("Middle Match Requirement")
        pyplot.ylabel("Num. Satisfying Pairs")
        pyplot.tight_layout() # Keeps the spacing nice.
        pyplot.plot(x_axis, y_axis, marker="x")

        pyplot.savefig("common_words_results.pdf", format="pdf")
        pyplot.cla()
        pyplot.close()


if __name__ == "__main__":
    main()
