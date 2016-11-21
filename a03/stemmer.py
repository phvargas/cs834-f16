import os
import sys
from time import strftime, localtime, time
from bs4 import BeautifulSoup
import Stemmer
from PyDictionary import PyDictionary


"""
This Python program
  1. takes as a command line argument a web page
  2. extracts the page
  3. extracts all the links from the page
  4. fron all the links from (3) goes back to (2) until no more links
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,November 5 at 23:11:30'
__email__ = 'pvargas@cs.odu.edu'


def get_top_words(filename, n):
    dictionary = PyDictionary()
    k = 0
    line_no = 0
    first_n = []
    is_english = ''
    with open(filename, 'r') as f:
        for line in f:
            line_no += 1
            word = line.split()[0]
            if len(line.split()) > 1:
                qty = int(line.split()[1])
            else:
                qty = 0
            print(word, line_no)
            try:
                print(word, word[0], is_english, k)
                if qty > 1 and word[0] >= 'a':
                    is_english = dictionary.meaning(word)
                    if is_english:
                        first_n.append(word)
                        k += 1
                        if k > n:
                            break
            except IndexError:
                print("Yes")
                pass

            print(k)
    print(first_n)

    with open('vocabulary.txt', 'w') as f:
        for word in first_n:
            f.write('%s\n' % word)

    f.close()

    return


if __name__ == '__main__':
    # checks for argument

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    get_top_words("sorted-collection.txt", 1000)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
