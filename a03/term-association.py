import os
import sys
import re
from time import strftime, localtime, time
from bs4 import BeautifulSoup
from collections import Counter
from math import log10

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

"""
term-association.py
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Tue, November 8 at 10:35:09'
__email__ = 'pvargas@cs.odu.edu'

inverted_index = {}
file_path = []
stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'wikipedia', 'is', 'by', 'was', 'for', 'on', 'from', 'edit', 'this',
              'as', 'with', '1', 'about', 'user', '3', 'it', 'page', 'he', 'free', 'that', 'at', 'registered', '2',
              'all', 'his', 'help', 'if', 'an', 'see', '^', 'c', 'under', 'u', 'window', 'contents', 'or', 'are',
              '2008', 'also', 'be', 's', '4', '5', '6', 'v', 'i', '0-86124-352-8', 'articlediscussioncurrent'
             ]


def main():
    # terms to calculate
    vocabulary = ['altarpiece', 'resurrection', 'retirement', 'football', 'country', 'system', 'book', 'california',
                  'department', 'washington']
    index_2add = []

    # get all urls
    with open('file-path.txt', 'r') as f:
        for url in f:
            file_path.append(url.strip())

    # get inverted index
    #with open('test.txt', 'r') as f:
    with open('inverted-file.txt', 'r') as f:
        for line in f:
            r = re.search('(^.*?):(.*)', line.strip())
            inverted_index[r.group(1)] = re.sub("[,\[\]\']", ' ', r.group(2)).split()

    print('Size of index:', len(inverted_index))

    for word in vocabulary:
        if word not in inverted_index:
            index_2add.append(word)

    build_index(index_2add)

    print('Size of index:', len(inverted_index))

    window = 5
    term_data = get_term_freq(vocabulary, window)

    assoc_measure = calc_assoc_measure(term_data)

    for term in assoc_measure:
        print(term,'\n====================================\n')
        print('{0:15} {1:15} {2:15} {3:15}'.format('MIM', 'EMIM', 'Chi-sqr', 'Dice\'s Coef'))
        print('-----------------------------------------------------------')
        r1 = sorted(assoc_measure[term], key=lambda l:l[1], reverse=True)
        r2 = sorted(assoc_measure[term], key=lambda l:l[2], reverse=True)
        r3 = sorted(assoc_measure[term], key=lambda l:l[3], reverse=True)
        r4 = sorted(assoc_measure[term], key=lambda l:l[4], reverse=True)

        mim = []
        for row in r1[:10]:
            mim.append(row[0])

        emim = []
        for row in r2[:10]:
            emim.append(row[0])

        chi = []
        for row in r3[:10]:
            chi.append(row[0])

        dice = []
        for row in r4[:10]:
            dice.append(row[0])

        for i in range(10):
            print('{0:15} {1:15} {2:15} {3:15}'.format(mim[i], emim[i], chi[i], dice[i]))

        print('\n')

    return


def calc_assoc_measure(data):
    assoc_measure = {}
    for term in data:
        assoc_measure[term] = []
        # calculate term frequency
        N_a = 0
        n = 0
        for file_index in inverted_index[term]:
            n += 1
            N_a += int(file_index.split(':')[1])
        mim = 0
        emim = 0
        chi_sqr = 0
        dice_coef = 0

        print('\n\n', term, N_a)
        print()
        for pairs in data[term]:
            if pairs[0] is not '_':
                N_ab = data[term]['_' + pairs]
                N_b = data[term][pairs]
                mim = N_ab / (N_a * N_b)
                emim = N_ab * log10(n * N_ab/(N_a * N_b))
                chi_sqr = (N_ab - 1 / n * N_a * N_b) ** 2 / (N_a * N_b)
                dice_coef = N_ab / (N_a + N_b)

                assoc_measure[term].append([pairs, mim, emim, chi_sqr, dice_coef])

                print('%s\t%.5f\t%.5f\t%.5f\t%.5f' % (pairs, mim, emim, chi_sqr, dice_coef))
    return assoc_measure


def build_index(vocabulary):
    global inverted_index, file_path
    file_no = 0

    for url in file_path:
        file_no += 1

        # get file content
        data = get_file_content(url)

        # get term frequency within document
        counts = Counter(data)

        # include term document frequency into index
        for word in vocabulary:
            if word in counts:
                inverted_index.setdefault(word, [])
                inverted_index[word].append('%d:%d' % (file_no, counts[word]))

    return


def get_term_freq(vocabulary, window):
    window_term = {}
    for term in vocabulary:
        window_term[term] = {}
        # get term frequency per document
        for file_index in inverted_index[term]:
            ptr = int(file_index.split(':')[0]) - 1
            # get file content
            data = get_file_content(file_path[ptr])
            print(ptr, file_path[ptr])

            # remove stop-words
            for value in stop_words:
                while value in data:
                    try:
                        data.remove(value)
                    except ValueError:
                        break

            counts = Counter(data)

            # get window terms
            pos = data.index(term)
            n = len(data)

            # get terms left-side of window
            left = pos - window
            if left < 0:
                left = 0

            left_window = data[left:pos]

            # get terms right-side of window
            right = pos + window + 1

            if right > n:
                right = n

            right_window = data[pos + 1:right]

            for value in right_window:
                if '_' + value not in window_term[term]:
                    window_term[term]['_' + value] = 1
                if value not in window_term[term]:
                    window_term[term][value] = counts[value]
                else:
                    window_term[term]['_' + value] += 1

            for value in left_window:
                if '_' + value not in window_term[term]:
                    window_term[term]['_' + value] = 1
                if value not in window_term[term]:
                    window_term[term][value] = counts[value]
                else:
                    window_term[term]['_' + value] += 1

            cycle = True
            while cycle or right < n:
                try:
                    pos += data[right + 1:].index(term) + window + 2

                    left = pos - window
                    left_window = data[left:pos]
                    for value in left_window:
                        if '_' + value not in window_term[term]:
                            window_term[term]['_' + value] = 1
                        if value not in window_term[term]:
                            window_term[term][value] = counts[value]

                    right = pos + window + 1
                    if right > n:
                        right = n

                    right_window = data[pos + 1:right]

                    for value in right_window:
                        if '_' + value not in window_term[term]:
                            window_term[term]['_' + value] = 1
                        if value not in window_term[term]:
                            window_term[term][value] = counts[value]

                except ValueError:
                    cycle = False
                    break

    return window_term


def get_file_content(url):
    # open file to get raw content
    f = open(url, 'r')
    page = f.read()
    f.close()

    soup = BeautifulSoup(page, 'html.parser')
    data = soup.body.get_text()
    data = re.sub('[*#/=?&>}{!<)(;,|\"\.\[\]]', ' ', data.lower())

    del page, soup

    return data.split()


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    main()

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
