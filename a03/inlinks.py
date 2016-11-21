import os
import sys
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import strftime, localtime, time
from hashlib import md5

"""
This Python program
  1. takes as a command line argument a web page
  2. extracts the page
  3. extracts all the links from the page
  4. fron all the links from (3) goes back to (2) until no more links
"""
__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  October 12, 2016 at 22:04:31'
__email__ = 'pvargas@cs.odu.edu'


def inlink(url, crawled_pages, link_count):
    if os.path.isfile(url):
        # initialize link count
        crawled_pages[url] = 0

        # read page
        f = open(url, 'r')
        page = f.read()
        f.close()

        print('Extracting links from: %s\n' % url)

        # create BeautifulSoup Object
        soup = BeautifulSoup(page, 'html.parser')

        # place source link into list
        for link in soup.find_all('a'):
            uri = link.get('href')
            if uri and uri[:3] == '../':
                uri = './en/' + re.search('(\.\.\/)+(.*)', uri).group(2)
                anchor_text = re.search('(.*>)(.*)(<\/a>)', str(link))
                if anchor_text:
                    print(uri, anchor_text.group(2))
                    link_count.setdefault(uri, 0)
                    link_count[uri] += 1

        return

    for filename in os.listdir(url):
        inlink(os.path.join(url, filename), crawled_pages, link_count)

    return


def top_inlinks(crawled_pages, link_count, n):
    for key in crawled_pages.keys():
        if key in link_count:
            crawled_pages[key] = link_count[key]

    # sort pages linked in descendant order
    data = sorted(crawled_pages.items(), key=lambda x:x[1], reverse=True)

    with open("anchor-text.txt", 'w') as f:
        print('Deleted anchort-text.txt')
    f.close()

    # print n anchor text
    for k in range(n):
        with open(data[k][0], 'r') as f:
            page = f.read()
        f.close()

        # create BeautifulSoup Object
        soup = BeautifulSoup(page, 'html.parser')

        # write anchor-tags
        with open("anchor-text.txt", 'a') as f:
            f.write('%s\n' % data[k][0])
            for link in soup.find_all('a'):
                anchor_text = re.search('(.*>)(.*)(<\/a>)', str(link))
                if anchor_text and anchor_text.group(2).strip():
                    print(anchor_text.group(2))
                    f.write('%s, ' % anchor_text.group(2))
            f.write('\n\n')

        f.close()

    print(data[:10])

    return

if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) != 2:
        print('Please, provide url\nUsage: python3 inlinks.py [url]')
        sys.exit(-1)

    #path = sys.argv[1]
    path = "./en"
    if not os.path.isdir(path):
        print('URL is invalid, please correct url and try again')
        sys.exit(1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # call crawler
    crawled_pages = {}
    link_count = {}
    inlink(path, crawled_pages, link_count)
    top_inlinks(crawled_pages, link_count, 10)
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
