import os
import sys
from time import strftime, localtime, time
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  October 10, 2016 at 07:58:10'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

data_dict = {}
data_bigram = {}
total_words = 0
total_bigrams = 0
passes = 0

def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    path = 'galagosearch-1.04/bin/CACM/'

    for filename in os.listdir(path):
        tokenize(os.path.join(path, filename))

    print(data_dict)
    data = sorted(data_dict.items(), key=lambda x:x[1], reverse=True)
    print(data[:20])

    with open('zipf_law.txt', 'w') as f:
        f.write('Word\t\value\n')
        for value, key in data:
            f.write('%s\t%s\n' % (value, key))

    print(len(data_dict), passes, total_words)
    print(len(data_bigram))
    data = sorted(data_bigram.items(), key=lambda x:x[1], reverse=True)
    print(data[:20])

    with open('zipf_law_bigram.txt', 'w') as f:
        f.write('Word\t\value\n')
        for value, key in data:
            f.write('%s\t%s\n' % (value, key))

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return


def tokenize(url):
    global passes, total_words, data_bigram, total_bigrams

    if os.path.isfile(url):
        passes += 1
        f = open(url, 'r')
        page = f.read()
        f.close()

        soup = BeautifulSoup(page, 'html.parser')
        data = soup.body.get_text()
        data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data)

        corpus = []


        # include unigram
        for unigram in data.split():
            unigram = unigram.lower()

            # remove empty string
            if len(unigram) > 0 and unigram != 's' and unigram != '-' and \
                    unigram != '–' and unigram != '—' and unigram != '--' and \
                    unigram != ' ':
                data_dict.setdefault(unigram, 0)
                data_dict[unigram] += 1
                corpus.append(unigram)
                total_words += 1
                print(unigram, end=', ')

        del data, page, soup

        # include bigram
        n = 1
        for words in corpus[:-1]:
            bigram = words + ' ' + corpus[n]
            n += 1
            data_bigram.setdefault(bigram, 0)
            data_bigram[bigram] += 1
            print(bigram, end=', ')

        print()

    if not os.path.isdir(url):
        return

    for filename in os.listdir(url):
        tokenize(os.path.join(url, filename))

    return


def file_tree(url, level):
    epoc_time = os.stat(url).st_mtime
    print('%s%s --> %s' % ('  '*level, url, strftime('%Y-%m-%d %H:%M:%S', localtime(epoc_time))))
    if not os.path.isdir(url):
        return

    for filename in os.listdir(url):
        tokenize(os.path.join(url, filename))
    return

if __name__ == '__main__':
    main()
    sys.exit(0)
