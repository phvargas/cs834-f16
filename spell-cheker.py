import os
import sys
from time import strftime, localtime, time


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

"""
spell-cheker.py
Create a simple spelling corrector based on the noisy channel model. Use a
single-word language model, and an error model where all errors with the same
edit distance have the same probability. Only consider edit distances of 1 or 2.
Implement your own edit distance calculator (example code can easily be found
on the Web).

"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Thr, November 10 at 15:58:47'
__email__ = 'pvargas@cs.odu.edu'


def main():
    max_distance = 2
    non_words = ['Teh', 'couse', 'tremmor', 'stodent']

    # upload collection
    dictionary = []
    with open('zipf_law.txt', 'r', encoding='iso-8859-1') as f:
        for word in f:
            dictionary.append(word.strip().split('\t'))

    for term in non_words:
        w_length = len(term)
        possible_list = []
        for word in dictionary:
            distance = abs(w_length - len(word[0]))
            if distance <= max_distance:
                possible_list.append(word[0].lower())

        collection_size = len(dictionary)

        short_list = distance_calc(term.lower(), possible_list)

        highest_prob = 0
        idx = 0
        for word in short_list:
            prob_w = float(dictionary[possible_list.index(word[0])][1]) / collection_size

            if highest_prob < prob_w:
                if abs(word[1] - len(term)) < max_distance:
                    highest_prob = prob_w
                    idx = possible_list.index(word[0])

        print('For %s the correct spelling is --> %s' % (term, possible_list[idx]))

    return


def distance_calc(word, possible_list):
    word_set = set([x for x in word])

    new_list = []
    distance = 2
    for p_word in possible_list:
        p_word_set = set([x for x in p_word])
        new_distance = len(p_word_set-word_set)

        if new_distance <= distance:
            new_list.append(p_word)
            distance = new_distance

    short_list = []
    max_count = 0
    for p_word in new_list:
        correct_count = 0
        i = 0
        for char in p_word:
            for k in range(i,len(word)):
                if char == word[k]:
                    correct_count += 1
                    i = k + 1
                    break

        if max_count < correct_count:
            max_count = correct_count
            short_list.append((p_word, max_count))

    print(short_list)

    return short_list


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    main()

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
