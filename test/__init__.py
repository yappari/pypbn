from glob import glob
import os
from pbn import parser
from pbn.lexer import lexer


def examples():
    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
    for fname in glob(
            os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'files/*')):
        yield os.path.join(files_dir, fname)
    


def test_lexer_new_game():
    lxr = lexer()
    
    lxr.input("""[Board "1"]\n  \t  \v  \r\n[Board "2"]""")
    assert 'NEWGAME' in [token.type for token in lxr]


def test_lexer_sample():
    for example in examples():
        lxr = lexer()
        with open(example) as exf:
            lxr.input(exf.read())
        for token in lxr:
            print token


def test_parser_simple():
    prs = parser()
    print prs.parse("""
        [A "B"]
% what?
        [B "C"]

        [C "D"]""")


def test_parser_sample():
    for example in examples():
        prs = parser()
        with open(example) as exf:
            print prs.parse(exf.read())
