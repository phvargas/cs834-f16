import os
import sys
from time import strftime, localtime, time
from datetime import datetime

__author__ = 'Plinio H. Vargas'
__date__ = 'Sat,  September 17, 2016 at 14:57:35'
__email__ = 'pvargas@cs.odu.edu'

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

def main():
    # record running time
    start = time()
    print('Starting Time: %s\n' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    path = '.\\documents'
    level = 1

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for filename in os.listdir(path):
        sitemap(os.path.join(path, filename), level)
    print('</urlset>')

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
    return


def sitemap(url, level):
    epoc_time = os.stat(url).st_mtime
    now = datetime.today()
    previous = datetime.strptime(strftime('%Y-%m-%d', localtime(epoc_time)), "%Y-%m-%d")
    no_days = (now - previous).days

    if no_days < 3:
        freq = 'daily'
    elif no_days < 32:
        freq = 'weekly'
    else:
        freq = 'monthly'

    sitmap_url = url.replace('\\', '/').strip('..')
    if os.path.isfile(url):
        print('<url>')
        print('  <loc>http://www.example.com{0}</loc>\n'.format(sitmap_url), end='')
        print('  <lastmod>{0}</lastmod>'.format(strftime('%Y-%m-%d', localtime(epoc_time))))
        print('  <changefreq>%s</changefreq>' % freq)
        print('</url>')
    if not os.path.isdir(url):
        return

    for filename in os.listdir(url):
        sitemap(os.path.join(url, filename), level + 1)
    return


def file_tree(url, level):
    epoc_time = os.stat(url).st_mtime
    print('%s%s --> %s' % ('  '*level, url, strftime('%Y-%m-%d %H:%M:%S', localtime(epoc_time))))
    if not os.path.isdir(url):
        return

    for filename in os.listdir(url):
        sitemap(os.path.join(url, filename), level + 1)
    return

if __name__ == '__main__':
    main()
    sys.exit(0)