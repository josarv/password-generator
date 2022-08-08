#!/usr/bin/env python3

from _version import __version__

import argparse
import random
import string
import math
import secrets


def check_length(value):
    ivalue = int(value)
    if not 7 <= ivalue <= 40:
        raise argparse.ArgumentTypeError('%s is not a valid password length' % value)
    return ivalue


def check_entropy(value):
    ivalue = int(value)
    if not 40 <= ivalue <= 256:
        raise argparse.ArgumentTypeError(
            '%s is not a valid password entropy value' % value)
    return ivalue


def main():
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-vo', '--verbose', help="increase output verbosity", action="store_true")
    parser.add_argument('-s', '--seed', help='UNSAFE - seed for the generator (deterministic mode)', action='store')
    group.add_argument('-l', '--length', help='set custom password length (default = 15 characters)', type=check_length, action='store')
    group.add_argument('-e', '--entropy', help='set custom password entropy (default = 96 bits)', type=check_entropy)
    args = parser.parse_args()
    available_characters = string.ascii_letters + string.digits + string.punctuation
    if args.length:
        length = args.length
        entropy = math.floor(length * math.log2(len(available_characters)))
    elif args.entropy:
        entropy = args.entropy
        length = math.ceil(entropy / math.log2(len(available_characters)))
    else:
        length = 15
        entropy = 96
    bits_per_char = round(entropy / length)
    if args.seed:
        random.seed(args.seed)
        print(''.join(random.choice(available_characters) for _ in range(length)))
    else:
        print(''.join(secrets.choice(available_characters) for _ in range(length)))
    if args.verbose:
        print(f'Password length: {length} characters')
        print(f'Password entropy: ~ {entropy} bits')
        print(f'Entropy per character: ~ {bits_per_char} bits')
        print(f'Character set size: {len(available_characters)} characters')


if __name__ == '__main__':
    main()
