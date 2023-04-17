import sys
import rlce

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('Action not recognized')
        sys.exit(0)

    if args[1] == 'genkey128':
        print('key128')
        ret = rlce.rlce_keypair(0, 'key128')
        if ret is None:
            print('ERROR CODE')
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
