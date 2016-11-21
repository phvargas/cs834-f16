import sys

__author__ = 'Plinio Hamar Vargas'
__date__ = '11/14/2016 10:35 AM'


def main():
    words = [
        'WIRELESS COMM/MOBILE COMPUTING',
        'COMPUTER ARCHITECTURE',
        'WEB SCIENCE',
        'SECUR CNCPT-PRTCL-PRGRM',
        'NO-SQL DATABASES',
        'DESIGN OF NETWORK PROTOCOLS',
        'ALGORITHMS AND DATA STRUCTURES',
        'OPERATING SYSTEMS',
        'SYSTEMS PROGRAMMING',
        'INTRO-NETWORKS & COMMUNICATION',
        'Database Concepts',
    ]

    for word in words:
        print(word.title())
    return


if __name__ == '__main__':
    main()
    sys.exit(0)