import argparse
from argparse import RawTextHelpFormatter
from Heuristics.good_suffix import GoodSuffix
from Heuristics.bad_character import BadCharacter
from Heuristics.last_character import LastCharacter
from Heuristics.bmhs2 import HorspoolSunday2
from Heuristics.next_to_last_character import NextToLastCharacter
from utils import get_alphabet
import boyer_moore as bm
import timeit

usage_example = '''Usage example:

 python main.py -c 1 2 -f C:\Desktop\Test1.fa -p ATGCATG
 python main.py -c 1 3 4 -f C:\Desktop\Test1.fa -p ATGCATG -b'''

parser = argparse.ArgumentParser(description='Boyer-Moore algorithm variants', formatter_class=RawTextHelpFormatter,
                                 epilog=usage_example, add_help=False)
required_parameters = parser.add_argument_group('required arguments')
optional_parameters = parser.add_argument_group('optional arguments')

required_parameters.add_argument("-c", "--case", type=int, metavar='', required=True, nargs='+', choices=range(1, 6),
                                 help="choose heuristic function (can combine multiple heuristics): \n"
                                      "1 - Good suffix rule; \n"
                                      "2 - Bad character rule; \n"
                                      "3 - Last character rule(BHS algorithm) \n"
                                      "4 - Next to last character rule(BMHS algorithm)\n"
                                      "5 - Horspool Sunday 2")
required_parameters.add_argument("-f", "--file", type=argparse.FileType('r', encoding='UTF-8'), metavar='',
                                 required=True,
                                 help="path to the file which represents string to be searched")
required_parameters.add_argument("-p", "--pattern", type=str, metavar='', required=True,
                                 help="pattern to be searched in text")

optional_parameters.add_argument("-b", "--benchmark", required=False, action="store_true",
                                 help="show time usage of the algorithm")
optional_parameters.add_argument("-h", "--help", action="help", help="show this help message and exit")

args = parser.parse_args()

heuristics = {
    1: GoodSuffix(),
    2: BadCharacter(),
    3: LastCharacter(),
    4: NextToLastCharacter(),
    5: HorspoolSunday2()
}


def parse_arguments():
    global alphabet
    alphabet = get_alphabet(args.file.read())
    args.file.seek(0)
    [bm.add_heuristic(heuristics.get(i)) for i in args.case]


def preprocess():
    bm.preprocess(args.pattern, alphabet)


if __name__ == '__main__':
    parse_arguments()
    preprocess()

    if args.benchmark:
        print(min(timeit.Timer('bm.boyer_moore(args.file.read())',
                               setup='from __main__ import args\nimport boyer_moore as bm').repeat(1, 5)))
    else:
        print(bm.boyer_moore(args.file.read()))

    args.file.close()

