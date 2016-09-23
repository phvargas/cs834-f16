import locale
import sys
import requests
import validators
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
__date__ = 'Mon,  September 19, 2016 at 20:35:11'
__email__ = 'pvargas@cs.odu.edu'

def crawler(url, crawled_pages):
    url = url.strip()

    # create hash for URI
    encoded_url = md5(url.encode()).hexdigest()
    if encoded_url in crawled_pages:
        print('%s already crawled..' % url)
        return

    crawled_pages[encoded_url] = url

    #locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    print('Extracting links from: %s\n' % url)

    # get uri status
    if requests.get(url).status_code != 200:
        print('\n\nURI is not available from SERVER. Verify URI.\n')
        return

    # get source from URI
    page = requests.get(url).text

    # get parse hostname from URI
    url = 'http://' + urlparse(url).netloc

    # create BeautifulSoup Object
    soup = BeautifulSoup(page, 'html.parser')

    # place source link into list
    for link in soup.find_all('a'):
        uri = link.get('href')
        try:
            # include hostname if url is provided by reference
            if ((len(uri) > 6 and uri[:7].lower() != 'http://') or len(uri) < 7) and uri[:8].lower() != 'https://':
                if uri[:2] == '//':    # if url has double backslash then url is not provided by reference
                    uri = 'http:' + uri
                elif uri[0] != '/':    # include backslash if it was not include by reference
                    uri = url + '/' + uri
                else:
                    uri = url + uri
        except TypeError:
            print('%s is invalid' % url)
            return

        # for debugging
        #print(uri)

        try:
            r = requests.head(uri)
            if 'Content-Type' in r.headers and r.headers['Content-Type'] == 'text/html':
                if r.status_code == 200:
                    crawler(uri, crawled_pages)
                elif 'location' in r.headers and (r.status_code == 301 or r.status_code == 302):
                    counter = 1
                    while counter < 7:
                        try:
                            uri = r.headers['location']
                            r = requests.head(r.headers['location'])
                            if 'location' in r.headers and (r.status_code == 301 or r.status_code == 302):
                                counter += 1
                            elif r.status_code == 200:
                                crawler(uri, crawled_pages)
                            else:
                                break
                        except KeyError:
                            print('Couldn\'t find resource for: %s' % url)
                            break

        except requests.exceptions.SSLError:
            print('Couldn\'t open: %s. URL requires authentication.' % uri)
        except requests.exceptions.ConnectionError:
            print('Couldn\'t open: %s. Connection refused.' % uri)

    return

if __name__ == '__main__':
    # checks for argument
    if len(sys.argv) != 2:
        print('Please, provide url\nUsage: python3 crawler.py [url]')
        sys.exit(-1)
    if not validators.url(sys.argv[1]):
        print('URL is invalid, please correct url and try again')
        sys.exit(1)

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # call crawler
    crawled_pages = {}
    crawler(sys.argv[1], crawled_pages)
    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    sys.exit(0)
    