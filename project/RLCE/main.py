import sys


if __name__ == '__main__':
    args = sys.argv

    if args[1] == 'genkey128':
        print('key128')
    elif args[1] == 'genkey192':
        print('key192')
    elif args[1] == 'genkey256':
        print('key256')
    elif args[1] == 'encr':
        print('encr')
    elif args[1] == 'kemenc':
        print('kemenc')
    elif args[1] == 'decr':
        print('decr')
