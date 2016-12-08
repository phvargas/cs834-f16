import os
import sys
from time import strftime, localtime, time
import re
from itertools import zip_longest
import numpy as np
from bs4 import BeautifulSoup

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  December 5, 2016 at 22:19:27'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # path for CACM collection
    path = '../galagosearch-1.04/bin/CACM/'

    # get words to compute Bernoulli probability
    words = {}
    word_matrix = []
    nomeclature = {'H': 'Hardware', 'S': 'Software'}

    with open('dataset.txt', 'r') as f:
        count = 0
        first_line = True
        for line in f:
            if not first_line:
                word = line.strip().split()
                words[word[0]] = count
                count += 1
            else:
                first_line = False

    # get words relevant to word-list
    count_words(path, words, word_matrix)

    #**************************************************************
    #         bernoulli_multiple
    #**************************************************************

    # create header for matrix
    header = create_header(words)
    n = len(header)   # number of term/words in training matrix
    for row in header:
        print(' & ', end='')
        for chr in row[:-1]:
            print(chr, end=' & ')
        print('%c & \\\\' % row[n-1])

    # print body of data
    n = len(words)
    i = 0
    for row in word_matrix:
        clss = row[n]
        fix_row = [x if x>0 else 1 for x in row[:n]]
        row = np.floor_divide(row[:n], fix_row)
        i += 1
        print(i, end=' & ')
        for string in row[:n - 1]:
            print(string, end=' & ')
        print('%d & %s\\\\' % (row[n-1], nomeclature[clss]))

    # print classifier multiple-bernoulli representation
    classifier, class_size = bernoulli_multiple(word_matrix)
    for row in classifier:
        print('%d & ' % np.sum(classifier[row]), end='')
        for string in classifier[row][:-1]:
            print(string, end=' & ')

        print('%d & %s\\\\' % (classifier[row][n-1], nomeclature[row]))

    # print classifier multiple-bernoulli results
    for row in classifier:
        print(' & ', end='')

        for freq in classifier[row]:
            print('%.3f' % ((freq + 1)/(class_size[row] + 1)), end=' & ')

        print('%s\\\\' % nomeclature[row])
    print('\n\n\n')

    #**************************************************************
    #         multinomial model
    #**************************************************************
    n = len(header)   # number of term/words in training matrix
    for row in header:
        print(' & ', end='')
        for chr in row[:-1]:
            print(chr, end=' & ')
        print('%c & \\\\' % row[n-1])

     # print body of data
    n = len(words)
    i = 0
    for row in word_matrix:
        clss = row[n]
        i += 1
        print(i, end=' & ')
        for string in row[:n - 1]:
            print(string, end=' & ')
        print('%d & %s\\\\' % (row[n-1], nomeclature[clss]))

    # print classifier  multinomial representation
    classifier = multinomial(word_matrix)
    for row in classifier:
        print('%d & ' % np.sum(classifier[row]), end='')
        for string in classifier[row][:-1]:
            print(string, end=' & ')

        print('%d & %s\\\\' % (classifier[row][n-1], nomeclature[row]))

    # print classifier multinomial model results
    v = len(words)   # number of feature
    for row in classifier:
        print(' & ', end='')
        freq_c = np.sum(classifier[row], axis=0)
        for freq in classifier[row]:
            print('%.3f' % ((freq + 1)/(freq_c + v)), end=' & ')

        print('%s\\\\' %  nomeclature[row])
    print('\n\n\n')
    #
    #
    print(words)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.4f seconds' % (time()-start))
    return


def bernoulli_multiple(matrix):
    n = len(matrix[0]) - 1  # number of term/words in training matrix

    # initialize c1 class vector
    df_c1 = [0 for x in range(n)]

    # initialize c2 class vector
    df_c2 = [0 for x in range(n)]

    # link classifier to rows
    classifier = {'H': df_c1, 'S': df_c2}
    class_size = {'H':0, 'S': 0}

    for row in matrix:
        fix_row = [x if x > 0 else 1 for x in row[:n]]    # fix div by 0 problem
        classifier[row[n]] = np.sum([np.floor_divide(row[:n], fix_row), classifier[row[n]]], axis=0)
        class_size[row[n]] += 1

    return classifier, class_size


def multinomial(matrix):
    n = len(matrix[0]) - 1  # number of term/words in training matrix

    # initialize c1 class vector
    df_c1 = [0 for x in range(n)]

    # initialize c2 class vector
    df_c2 = [0 for x in range(n)]

    # link classifier to rows
    classifier = {'H': df_c1, 'S': df_c2}

    for row in matrix:
        classifier[row[n]] = np.sum([row[:n], classifier[row[n]]], axis=0)

    return classifier


def count_words(url, words, word_matrix):
    # get hardware training file
    hardware = []
    with open('hardware.txt', 'r') as f:
        for line in f:
            hardware.append(line.strip() + '.html')

    software = []
    with open('software.txt', 'r') as f:
        for line in f:
            software.append(line.strip() + '.html')

    for filename in os.listdir(url):
        if filename in hardware or filename in software:
            f = open(os.path.join(url, filename), 'r')
            page = f.read()
            f.close()

            print(url)
            soup = BeautifulSoup(page, 'html.parser')
            data = soup.get_text()
            data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data)


            # find all features and increment frequency
            row = [0 for x in range(len(words))]
            for unigram in data.split():
                unigram = unigram.lower()

                # remove empty string
                if len(unigram) > 0 and unigram != 's' and unigram != '-' and \
                        unigram != '–' and unigram != '—' and unigram != '--' and \
                        unigram != ' ':
                    unigram = unigram.strip("'")
                    if unigram in words:
                        row[words[unigram]] += 1

            if filename in hardware:
                row.append('H')
            else:
                row.append('S')

            word_matrix.append(row)
            del data, page, soup

    return


def create_header(words):
    text = ''
    for str, index in sorted(words.items(), key=lambda x:x[1]):
        text += str + ' '

    header = []
    for x in zip_longest(*text.split(), fillvalue=' '):
        header.append(list(x))

    header = np.array(header)
    header = header.transpose()

    n = len(header)   # number of term/words in training matrix
    for i in range(n):
        cont = 0
        for chr in header[i]:
            if chr == ' ':
                cont += 1

        header[i] = np.roll(header[i], cont)

    return header.transpose()


if __name__ == '__main__':
    main()
    sys.exit(0)