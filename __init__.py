from ply import yacc
from lexer import tokens


class Tag(object):
    def __init__(self, name, string):
        self.name = name
        self.string = string

    def __repr__(self):
        return "Tag(%s: %s)" % (self.name, self.string)


class Call(object):
    irreg_i = False
    nag = None
    note = None
    suffix = None

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "Call(%s)" % ''.join(
            str(x) for x in (
                '^I' if self.irreg_i else '',
                self.text, self.suffix, self.note, self.nag
            ) if x)

class MoreCalls(Call):
    text = '*'

    def __init__(self):
        pass

class ContCalls(Call):
    text = '+'

    def __init__(self):
        pass

class IrregS(Call):
    text = '^S'

    def __init__(self):
        pass



class CardPlay(object):
    irreg_r = False
    irreg_l = False
    nag = None
    note = None
    suffix = None

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return "CardPlay(%s)" % ''.join(
            str(x) for x in (
                '^R' if self.irreg_r else '',
                '^L' if self.irreg_l else '',
                self.text, self.suffix, self.note, self.nag
            ) if x)

class MoreCards(CardPlay):
    text = '*'

    def __init__(self):
        pass

class ContCards(CardPlay):
    text = '+'

    def __init__(self):
        pass



def p_term_auction(p):
    """auction : tag auction_body"""
    assert p[1].name == 'Auction'
    p[0] = p[1], p[2]


def p_term_play(p):
    """play : tag play_body"""
    assert p[1].name == 'Play'
    p[0] = p[1], p[2]


def p_term_call(p):
    """call : CALL"""
    p[0] = Call(p[1])

def p_term_irreg_s(p):
    """call : IRREG_S"""
    p[0] = IrregS()

def p_term_more_calls(p):
    """call : MORE_CALLS"""
    p[0] = MoreCalls()

def p_term_cont_calls(p):
    """call : CONT_CALLS"""
    p[0] = ContCalls()

def p_term_call_suffix(p):
    """call : call SUFFIX"""
    p[1].suffix = p[2]
    p[0] = p[1]

def p_term_call_note(p):
    """call : call NOTE"""
    p[1].note = p[2]
    p[0] = p[1]

def p_term_call_nag(p):
    """call : call NAG"""
    p[1].nag = p[2]
    p[0] = p[1]

def p_term_irreg_i(p):
    """call : IRREG_I call"""
    p[1].irreg_i = True
    p[0] = p[1]



def p_term_card(p):
    """card : CARD"""
    p[0] = CardPlay(p[1])

def p_term_more_cards(p):
    """card : MORE_CARDS"""
    p[0] = MoreCards()

def p_term_cont_cards(p):
    """card : CONT_CARDS"""
    p[0] = ContCards()

def p_term_card_suffix(p):
    """card : card SUFFIX"""
    p[1].suffix = p[2]
    p[0] = p[1]

def p_term_card_note(p):
    """card : card NOTE"""
    p[1].note = p[2]
    p[0] = p[1]

def p_term_card_nag(p):
    """card : card NAG"""
    p[1].nag = p[2]
    p[0] = p[1]

def p_term_card_irreg_r(p):
    """card : IRREG_R card"""
    p[1].irreg_r = p[2]
    p[0] = p[1]

def p_term_card_irreg_l(p):
    """card : IRREG_L card"""
    p[1].irreg_l = p[2]
    p[0] = p[1]

    

def p_term_game_list_basic(p):
    """game_list : game"""
    p[0] = [p[1]]


def p_term_game_list(p):
    """game_list : game_list NEWGAME
                 | game_list NEWGAME game
    """
    games = p[1]
    if len(p) > 3:
        games += [p[3]]
    p[0] = games
    

def p_term_list(p):
    """auction_body : call
                    | call auction_body
       play_body    : card
                    | card play_body
       game         : tag
                    | auction
                    | play
                    | tag game
                    | auction game
                    | play game
    """
    p[0] = [p[1]]
    if len(p) > 2:
        p[0] += p[2]

# PBN-1.0 3.3
def p_term_tag(p):
    "tag : LBRACKET NAME STRING RBRACKET"
    p[0] = Tag(p[2], p[3])

def parser():
    return yacc.yacc(start='game_list')

