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
    graph = {'A': {'A':[0, 0]},
             'B': {'o':['A'], 'B':[0, 0]},
             'C': {'o':['A', 'B', 'D'], 'C':[0, 0]},
             'D': {'D':[0, 0]},
             'E': {'o':['D'], 'E': [0, 0]},
             'F': {'o':['D'], 'F': [0, 0]},
             'G': {'G':[0, 0]}}

    node_value = {'A': [1, 1], 'B': [1, 1],'C': [1, 1],'D': [1, 1],'E': [1, 1],'F': [1, 1],'G': [1, 1]}

    for k in range(5):
        hub_total = 0
        auth_total = 0
        for node in graph:
            if 'o' in graph[node]:
                for vertex in graph[node]['o']:
                    graph[node][node][1] += node_value[vertex][0]
                    graph[vertex][vertex][0] += node_value[node][1]
                    hub_total += node_value[vertex][0]
                    auth_total += node_value[node][1]

        for node in graph:
            node_value[node][0] = graph[node][node][0] / auth_total
            node_value[node][1] = graph[node][node][1] / hub_total
            graph[node][node][0] = 0
            graph[node][node][1] = 0

        print('\nfor k=%d HITS Calculation is:' % (k + 1))
        for node in sorted(node_value):
            print('%c = (%.2f, %.2f)' % (node, node_value[node][0], node_value[node][1]))

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.4f seconds' % (time()-start))
    return


if __name__ == '__main__':
    main()
    sys.exit(0)