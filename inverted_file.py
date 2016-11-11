import os
import sys
import re
from time import strftime, localtime, time
from bs4 import BeautifulSoup
from collections import Counter

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

"""
Cluster.py
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Mon ,November 7 at 7:49:11'
__email__ = 'pvargas@cs.odu.edu'

file_no = 0
word_index = {}
file_path = []


def create_index(path, term_file):
    vocabulary = []
    with open(term_file, 'r') as f:
        for word in f:
            vocabulary.append(word.strip())

    get_url(path, vocabulary)

    # store inverted file
    with open('inverted-file.txt', 'w') as f:
        for index in word_index:
            print(index, word_index[index])
            f.write('%s:%s\n' % (index, word_index[index]))

    # store file path
    with open('file-path.txt', 'w') as f:
        for path in file_path:
            f.write('%s\n' % path)

    return


def get_url(url, vocabulary):
    global file_no, word_index, file_path
    if os.path.isfile(url):
        file_no += 1
        print(file_no, url)
        file_path.append(url)

        # get file content
        f = open(url, 'r')
        page = f.read()
        f.close()

        soup = BeautifulSoup(page, 'html.parser')
        data = soup.body.get_text()
        data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data.lower())

        counts = Counter(data.split())

        for word in vocabulary:
            if word in counts:
                word_index.setdefault(word, [])
                word_index[word].append('%d:%d' % (file_no, counts[word]))
                print('%s %d:%d' % (word, file_no, counts[word]), end=',')
        print()
        del data, page, soup

    if not os.path.isdir(url):
        return

    for filename in os.listdir(url):
        get_url(os.path.join(url, filename), vocabulary)

    return

if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    create_index('./en', 'vocabulary.txt')

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
