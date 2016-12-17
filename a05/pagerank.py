import os
import sys
from time import strftime, localtime, time
from nltk.corpus import reuters
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
import gzip
from sklearn.feature_extraction.text import TfidfVectorizer

__author__ = 'Plinio H. Vargas'
__date__ = 'Wed,  December 14, 2016 at 16:29:11'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

cachedStopWords = stopwords.words("english")


def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # creating the graph

    graph = {'A': {'links': ['B', 'C'], 'size': 0, 'pr': 0},
             'B': {'links': ['C'], 'size': 1, 'pr': 0},
             'C': {'links': [], 'size': 3, 'pr': 0},
             'D': {'links': ['C', 'E', 'F'], 'size': 0, 'pr': 0},
             'E': {'links': [], 'size': 1, 'pr': 0},
             'F': {'links': [], 'size': 1, 'pr': 0},
             'G': {'links': [], 'size': 0, 'pr': 0}}
    """
    graph = {'A': {'links':['C'], 'size': 2, 'pr': 0},
             'B': {'links': ['A'], 'size':1, 'pr': 0},
             'C': {'links': ['A', 'B'], 'size': 1, 'pr': 0}}
    """
    landa = 0.15
    n = len(graph)
    # pr = {'A': 1/n, 'B': 1/n, 'C': 1/n}
    pr = {'A': 1/n, 'B': 1/n, 'C': 1/n, 'D': 1/n, 'E': 1/n, 'F': 1/n, 'G': 1/n}
    y = lambda x: graph[x]['links']
    l = lambda x: 1 if graph[x]['size'] == 0 else graph[x]['size']
    page_rank = lambda k: landa/n + (1 - landa) * sum([pr[x]/l(x) for x in y(k)])

    for k in range(5):
        print('Iteration k=%d:' % k)
        for node in sorted(graph):
            graph[node]['pr'] = page_rank(node)
            print('PR(%c) = %.4f' % (node, graph[node]['pr']))

        for node in graph:
            pr[node] = graph[node]['pr']
        print()

    """
    print('for k=%d HITS Calculation is:\n' % (k + 1))
    for node in sorted(node_value):
        print('%c = (%.2f, %.2f)' % (node, node_value[node][0], node_value[node][1]))
    """

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.4f seconds' % (time()-start))
    return


if __name__ == '__main__':
    main()
    sys.exit(0)