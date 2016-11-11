import os
import sys
import re
import operator
from time import strftime, localtime, time
from bs4 import BeautifulSoup
import Stemmer

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

"""
Cluster.py
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Sat ,November 5 at 23:11:30'
__email__ = 'pvargas@cs.odu.edu'

window = 100
inverted_index = {}
file_path = []


def get_top_words(filename):
    stemmer = Stemmer.Stemmer('english')
    cluster = {}

    # stem and cluster n-top words in sorted collection
    with open(filename, 'r') as f:
        for word in f:
            word = word.strip()
            stem = stemmer.stemWord(word)
            cluster.setdefault(stem, [])
            cluster[stem].append(word)

    # calculate dice's coefficient for cluster pairs
    for values in sorted(cluster.items(), key=operator.itemgetter(1)):
        values = values[0]

        # add cluster header
        f = open('cluster-association.txt', 'a')

        print()
        f.write('\n')
        print(values, cluster[values])
        f.write('%s - %s\n' % (values, cluster[values]))
        f.close()

        if len(cluster[values]) > 1:
            # get number of pairs in cluster
            n = len(cluster[values]) - 1
            n = int(n * (n + 1) / 2)

            # initialize pair frequency
            window_freq = [0 for x in range(n)]

            dice_coefficient(cluster[values], window_freq)

    return


def dice_coefficient(pairs, window_freq):
    global window

    # add cluster header
    f = open('cluster-association.txt', 'a')

    # calculate pair coefficient
    for i in range(len(pairs)):
        for k in range(i + 1, len(pairs)):
            print('\t', pairs[i], pairs[k], end=' -- dice-coef:')
            f.write(('\t (%s, %s) -- dice-coef:' % (pairs[i], pairs[k])))

            # inverted_index[pairs[i]] contains documents for first pair element
            pair1 = [x.split(':') for x in inverted_index[pairs[i]]]
            pair2 = [x.split(':') for x in inverted_index[pairs[k]]]

            # find files where term intersect
            no_intercept = 0
            for files in pair1:
                if files[0] in [x[0] for x in pair2]:
                    no_intercept += 1
                    url = file_path[int(files[0])]

                    """
                    f = open(url, 'r')
                    page = f.read()
                    f.close()

                    soup = BeautifulSoup(page, 'html.parser')
                    data = soup.body.get_text()
                    data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data)

                    del data, page, soup
                    """

            print('%.4f' % (2 * no_intercept / (len(pair1) + len(pair2))))
            f.write(('%.4f\n' % (2 * no_intercept / (len(pair1) + len(pair2)))))
    f.close()
    return

if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # get inverted index
    with open('inverted-file.txt', 'r') as f:
        for line in f:
            r = re.search('(^.*?):(.*)', line.strip())
            inverted_index[r.group(1)] = re.sub("[,\[\]\']", ' ', r.group(2)).split()

    # get all filenames in the collection
    with open('file-path.txt', 'r') as f:
        for line in f:
            file_path.append(line.strip())

    # remove cluster-association.txt file
    f = open('cluster-association.txt', 'w')
    f.close()

    get_top_words("vocabulary.txt")

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
