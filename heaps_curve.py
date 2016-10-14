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
heaps_data = []
total_words = 0
passes = 0

def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    path = './en'

    for filename in os.listdir(path):
        tokenize(os.path.join(path, filename))

    print(data_dict)
    print(len(data_dict), passes, total_words)

    with open('heaps_curve.txt', 'w') as f:
        f.write('words\n' )
        for value in heaps_data:
            f.write('%d\n' % value)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return


def tokenize(url):
    global passes, total_words, data_bigram

    if os.path.isfile(url):
        passes += 1
        f = open(url, 'r')
        page = f.read()
        f.close()

        soup = BeautifulSoup(page, 'html.parser')
        data = soup.body.get_text()
        data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data)

        # include unigram
        for unigram in data.split():
            unigram = unigram.lower()

            # remove empty string
            if len(unigram) > 0 and unigram != 's' and unigram != '-' and \
                    unigram != '–' and unigram != '—' and unigram != '--' and \
                    unigram != ' ':
                data_dict.setdefault(unigram, 0)
                data_dict[unigram] += 1
                total_words += 1

                print(unigram, end=', ')

        heaps_data.append(len(data_dict))
        del data, page, soup

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