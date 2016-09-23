import os
import sys
import hashlib
from stop_words import get_stop_words
from time import strftime, localtime, time

__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  September 17, 2016 at 14:57:35'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

def main():
    return


def simhash(data):
    # remove stop words from file
    clean_data = [x for x in data.split() if x not in stop_words]

    # initialize weight vector
    weight_vector = [0 for x in range(128)]

    # find frequency of words by putting them into a dictionary
    data_dict = {}
    for word in clean_data:
        data_dict.setdefault(word, 0)
        data_dict[word] += 1

    # hash words using python text hash function
    for word in data_dict.keys():
        hash_data = hashlib.md5("{0}".format(word).encode()).hexdigest()
        binary = bin(int(hash_data, 16))[2:]
        while len(binary) < 128:
            binary = '0' + binary
        k = 0
        for x in binary:
            if int(x):
                weight_vector[k] += data_dict[word]
            else:
                weight_vector[k] -= data_dict[word]
            k += 1

    binary = ''
    for v in weight_vector:
        if v < 1:
            binary += '0'
        else:
            binary += '1'
    print(binary)
    return


if __name__ == '__main__':
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    stop_words = get_stop_words('en')

    path = '.\\test-data'
    for filename in [x for x in os.walk(path)][0][2]:
        with open(path + '\\'  +filename, 'r') as f:
            simhash(f.read())
        f.close()

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)