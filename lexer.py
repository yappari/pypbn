import re
from ply import lex


states = (
    ('tag', 'exclusive'),
    ('inline', 'inclusive'),
)

tokens = (
    'NEWGAME',
    
    'LBRACKET',
    'RBRACKET',

    'NAME',
    'STRING',

    'CALL',
    'CARD',
    'SUFFIX',
    'NOTE',
    'NAG',
    'MORE_CALLS',
    'MORE_CARDS',
    'CONT_CALLS',
    'CONT_CARDS',
    'IRREG_I',
    'IRREG_S',
    'IRREG_R',
    'IRREG_L',
)

# PBN 2.3: Line specification
def t_inline_NEWLINE(t):
    r'\n'
    t.lexer.begin('INITIAL')

# PBN 2.4: Escape mechanism
def t_INITIAL_ESCAPE(t):
    r'%[^\n]*\n'

# PBN 3: Game Layout
def t_INITIAL_NEWGAME(t):
    r'(\s*\n)'
    t.value = ''
    return t

# PBN 3.2: Tokens
def t_LBRACKET(t):
    r'\['
    t.value = ''
    t.lexer.begin('tag')
    return t

def t_tag_RBRACKET(t):
    r'\]'
    t.value = ''
    t.lexer.begin('inline')
    return t

def t_tag_NAME(t):
    r'[A-Za-z0-9_]+'
    t.lexer.last_tag = t.value
    return t

def t_tag_STRING(t):
    r'"([^"\\]|\\[\\"\d])*"'
    t.value = re.sub(r'\\(["\\"])', '\\1', t.value[1:-1])
    return t

# what about it?
#t_CALL = r'[CDHS][2-9TJQKA]|-'
def t_CALLCARD(t):
    r'[-A-Za-z0-9]+'
    t.lexer.begin('inline')
    if t.lexer.last_tag == 'Auction':
        t.type = 'CALL'
    elif t.lexer.last_tag == 'Play':
        t.type = 'CARD'
    else:
        return
    return t

def t_inline_SUFFIX(t):
    r'[\?!]{1,2}'
    if t.lexer.last_tag not in ('Auction', 'Play'):
        return
    return t

def t_inline_NOTE(t):
    r'=\d+='
    if t.lexer.last_tag not in ('Auction', 'Play'):
        return
    t.value = int(t.value[1:-1])
    return t

def t_inline_NAG(t):
    r'\$\d+'
    if t.lexer.last_tag not in ('Auction', 'Play'):
        return
    t.value = int(t.value[1:])
    return t

def t_ASTER(t):
    r'\*'
    t.lexer.begin('inline')
    if t.lexer.last_tag == 'Auction':
        t.type = 'MORE_CALLS'
    elif t.lexer.last_tag == 'Play':
        t.type = 'MORE_CARDS'
    else:
        return
    t.value = ''
    return t

def t_PLUS(t):
    r'\+'
    t.lexer.begin('inline')
    if t.lexer.last_tag == 'Auction':
        t.type = 'CONT_CALLS'
    elif t.lexer.last_tag == 'Play':
        t.type = 'CONT_CARDS'
    else:
        return
    t.value = ''
    return t

def t_IRREGULARITY(t):
    r'\^[ISRL]'
    t.lexer.begin('inline')
    if t.lexer.last_tag not in ('Auction', 'Play'):
        return
    t.type = 'IRREG_' + t.value[1]
    t.value = ''
    return t


def t_COMMENT(t):
    r'{[^}]*}'
    t.lexer.begin('inline')


def t_ANY_error(t):
    print "Illegal character '%s'" % t.value[0]


t_ANY_ignore = ' \t\v\r'

def lexer(**kwargs):
    lexer = lex.lex(**kwargs)
    lexer.last_tag = ''
    return lexer
