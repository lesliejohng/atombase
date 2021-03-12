import pytest
from fenChecker import Fen, WarningMsg
import mock

startingFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# -------------------- Fixtures -----------------------------------------------

@pytest.fixture
def good_fen():
    # sets up a Fen object with a valid fen
    # postion after 1 e4 e5 2 Nf3
    return Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

@pytest.fixture
def good_ep_fen():
    # sets up a Fen object with a valid test.ep square
    # NB I am currently not clear whether this should be set ONLY if there is
    # an enemy pawn positioned to perform a ep capture. ie only when it matters!
    # The following position is after 1 e4 e6 2 e5 d5 when white could play
    # 3 exd6 e.p.
    return Fen('rnbqkbnr/pppp1ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3')

@pytest.fixture
def castling_fen():
    # in this position it is not clear whether or not the Kings or Rooks
    # have moved as each Rook could have moved and moved back and the kings
    # could have moved and directly moved back or taken a triangluar
    # route back to their original square.
    return Fen('r1bqkb1r/ppp2ppp/2np1n2/4p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R')
    # toPlay, castling and ep will need to be set
# -----------------------------------------------------------------------------

# -------------------- assumptions --------------------------------------------

# In handling a string input I have made the following assumptions
#       1) the first sub-string is always the board
#       2) the last sub-string is always the move counter IF A DIGIT and fen
#          has more at least 2 elements
#       3) the penultimate sub-string is always the half move clock IF A DIGIT
#          AND the last sub-string is ALSO A DIGIT and the fen has as least
#          3 elements
#       4) if a toPlay, castling or ep element is recognised
#          anywhere in the fen that value will be saved

# -----------------------------------------------------------------------------

# -------------------- tests: non-string fen ----------------------------------

def test_missingFen():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # full reset to starting position
        # currently this is not an automatic reset to the starting position
        # as in pychess, but requires manual input of each element
        # of the fen
        test = Fen() # nothing passed
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen

def test_nonStringFenInteger():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # reset to starting position
        test = Fen(fen = 5) # integer passed
        # 5 is a valid fen character, so the board element consists of 5
        # blank squares
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen

def test_nonStringFenFloat():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # reset to starting position
        test = Fen(fen = 5.45) # float passed
        # 5.45 could be read as a board with 10 squares and one invalid
        # character ('.')
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen

def test_nonStringFenBool():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # full reset to starting position
        test = Fen(True) # bool passed
        # 5 is a valid fen character, so the board element consists of 5
        # blank squares
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen

# ------------------------------------------------------------ 4 tests: total 4

# -------------------- test sub-string assumptions ----------------------------

def test_noBoardSubstring():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R']):
        test = Fen(fen = 'w KQkq - 5 20')
        # toPlay, castling and ep should be recognised
        # no board element passed
        # last two items accepted as they are digits
        assert test.fenElements == ['w', 'KQkq', '-', '5', '20']
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        # fenToPlay set to test default 'w'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '5'
        assert test.move == '20'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 5 20'

def test_singleDigit():
        # the available digit should be taken as the move number
        # half move will be reset to o
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 2'

def test_NoDigit():
        # the available digit should be taken as the move number
        # half move will be reset to 0, move to 1
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq -')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1'

def test_MisplacedDigitsboth():
        # misplaced digits will be reset
        # half move will be reset to 0, move to 1
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w 1 2 KQkq -')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1'

def test_MisplacedDigitsOne():
        # misplaced digits will be reset
        # half move will be reset to 0
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w 1 KQkq - 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        # the last digit is assumed to be the move counter
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 2'

# ------------------------------------------------------------ 5 tests: total 9

# -------------------- fen passed with missing elements -----------------------

def test_FenBoardOnly():
    with mock.patch('builtins.input',side_effect = ['w','KQkq','-']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq 1 2')
        # reset all but board and halfMove/move, as missing element
        # requires input of all other elements of the fen
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'

def test_fenMissingBoard():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R']):
        test = Fen(fen = 'w KQkq - 1 2')
        # reset all but board and halfMove/move, as missing element
        # requires input of all other elements of the fen
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'

def test_fenMissingToPlay():
    with mock.patch('builtins.input',side_effect = ['w']):
        test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR KQkq d6 0 3')
        # position after 1 e4 e6 2 e5 d5
        # the missing toPlay would make it impossible to check ep,
        # but toPlay should be set in time to prevent  problem
        assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingCastling():
    with mock.patch('builtins.input',side_effect = ['KQkq']):
        test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w d6 0 3')
        assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingEP():
    with mock.patch('builtins.input',side_effect = ['d6']):
        test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq 0 3')
        assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingDigit():
    test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 3')
    # assumed that the provided digit is the move number
    # half move will be reset to 0
    assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

# ----------------------------------------------------------- 6 tests: total 15

# -------------------- test allocation of '-' ---------------------------------

def test_ep_None():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_castling_None_EPwrong():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    # no enemy pawns in place so reset to '-'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_castling_None_EPok():
    test = Fen(fen = 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R b - e3 1 2')
    # position after 1 Nf3 d5 2 Nc3 d4 3 e4: e3 is a ep square
    assert test.board == 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    # e3 is valid
    assert test.ep == 'e3'
    assert test.halfMove == '0' # last move was pawn move

    assert test.move == '2'

def test_castling_ep():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_2Blanks_castling_set():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - - KQkq 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_2Blanks_ep_setIncorrectly():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - -  e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    assert test.ep == '-' # e3 inconsistant with board
    assert test.halfMove == '1'
    assert test.move == '2'

def test_2Blanks_ep_setCorrectly():
    test = Fen(fen = 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R b - -  e3 1 2')
    # 1 Nf3 d5 2 Nc3 d4 3 e4 - e3 valid
    assert test.board == 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    assert test.ep == 'e3'
    assert test.halfMove == '0' # last move was pawn move
    assert test.move == '2'

# ----------------------------------------------------------- 7 tests: total 22

# -------------------- test of extra white spaces -----------------------------

def test_fenWhiteSpaceBetweenElements():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR  w     KQkq d6 0  3')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-' #d6 inconsistant with board
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

def test_fenLeadingWhiteSapce():
    test = Fen(fen = '        rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq d6 0  3')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-' # d6 inconsistant with board
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

def test_fenTrailingWhiteSpace():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR  w KQkq d6 0 3     ')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-' # d6 inconsistant with board
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

def test_fenWhiteSpaceInCastling():
    with mock.patch('builtins.input',side_effect = ['KQkq']):
        # problem this would result in two valid castling elements
        # should be caught as contradictory and require input of castling
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQ kq d6 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-' # d6 inconstsant with board
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

def test_fenWhiteSpaceInEP():
    with mock.patch('builtins.input',side_effect = ['d6']):
        # problem this would result in two valid castling elements
        # should be caught as contradictory and require input of castling
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq d 6 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-' #d6 incosistant with board
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

def test_fenWhiteSpaceInCandEP():
    with mock.patch('builtins.input',side_effect = ['KQkq', 'd6']):
        # problem this would result in two valid castling elements
        # should be caught as contradictory and require input of castling
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w K Qkq d 6 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-' # d6 inconsistent with board
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR w KQkq - 0 3'

# -----------------------------------------------------------  6 test: total 28

# -------------------- fen elements incorrect ---------------------------------

def test_toPlayError():
    with mock.patch('builtins.input',side_effect = ['w']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_CastlingError():
    with mock.patch('builtins.input',side_effect = ['KQkq', '-']):
        # as the castling element is unrecognisable, '-'
        # cannot be allocated, so ep needs to be set
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_epError():
    with mock.patch('builtins.input',side_effect = ['-']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq x 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

# ----------------------------------------------------------- 3 tests: total 31

# -------------------- ep invalid squares -------------------------------------

def test_epInvalidSquare():
    with mock.patch('builtins.input',side_effect = ['-']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        # manual reset ep to '-'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_epwtpValid():
    test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKB1R w KQkq d6 0 3')
    # after 1 e4 e6 2 e5 d4: e6 correct
    assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'

def test_epbtpValid():
    test = Fen(fen = 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq e3 0 4')
    # after 1 Nf3 d5 2 Nc3 d4 3 e4: e3 correct
    assert test.board == 'rnbqkbnr/ppp1pppp/8/8/3pP3/2N2N2/PPPP1PPP/R1BQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == 'e3'
    assert test.halfMove == '0'
    assert test.move == '4'

def test_epwtpInvalid():
    with mock.patch('builtins.input',side_effect = ['-']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        # temporary: reset fentest.ep to '-'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_epbtpInvalid():
    with mock.patch('builtins.input',side_effect = ['-']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        # ep reset to '-'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_ep_a6_correct():
    test = Fen('4k3/8/8/pP6/8/8/8/4K3 w - a6 0 1')
    assert test.ep == 'a6'

def test_ep_a6_incorrect():
    test = Fen('4k3/8/8/p1P5/8/8/8/4K3 w - a6 0 1')
    assert test.ep == '-'

def test_ep_b6_correctRA():
    test = Fen('4k3/8/8/1pP5/8/8/8/4K3 w - b6 0 1')
    assert test.ep == 'b6'

def test_ep_b6_correctLA():
    test = Fen('4k3/8/8/Pp6/8/8/8/4K3 w - b6 0 1')
    assert test.ep == 'b6'

def test_ep_b6_incorrect():
    test = Fen('4k3/8/8/1p1P4/8/8/8/4K3 w - b6 0 1')
    assert test.ep == '-'

def test_ep_c6_correctRA():
    test = Fen('4k3/8/8/2pP4/8/8/8/4K3 w - c6 0 1')
    assert test.ep == 'c6'

def test_ep_c6_correctLA():
    test = Fen('4k3/8/8/1Pp5/8/8/8/4K3 w - c6 0 1')
    assert test.ep == 'c6'

def test_ep_c6_incorrect():
    test = Fen('4k3/8/8/2p1P3/8/8/8/4K3 w - c6 0 1')
    assert test.ep == '-'

def test_ep_d6_correctRA():
    test = Fen('4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1')
    assert test.ep == 'd6'

def test_ep_d6_correctLA():
    test = Fen('4k3/8/8/2Pp4/8/8/8/4K3 w - d6 0 1')
    assert test.ep == 'd6'

def test_ep_d6_incorrect():
    test = Fen('4k3/8/8/3p1P2/8/8/8/4K3 w - d6 0 1')
    assert test.ep == '-'

def test_ep_e6_correctRA():
    test = Fen('4k3/8/8/4pP2/8/8/8/4K3 w - e6 0 1')
    assert test.ep == 'e6'

def test_ep_e6_correctLA():
    test = Fen('4k3/8/8/3Pp3/8/8/8/4K3 w - e6 0 1')
    assert test.ep == 'e6'

def test_ep_e6_incorrect():
    test = Fen('4k3/8/8/4p1P1/8/8/8/4K3 w - e6 0 1')
    assert test.ep == '-'

def test_ep_f6_correctRA():
    test = Fen('4k3/8/8/5pP1/8/8/8/4K3 w - f6 0 1')
    assert test.ep == 'f6'

def test_ep_f6_correctLA():
    test = Fen('4k3/8/8/4Pp2/8/8/8/4K3 w - f6 0 1')
    assert test.ep == 'f6'

def test_ep_f6_incorrect():
    test = Fen('4k3/8/8/5p1P/8/8/8/4K3 w - f6 0 1')
    assert test.ep == '-'

def test_ep_g6_correctRA():
    test = Fen('4k3/8/8/6pP/8/8/8/4K3 w - g6 0 1')
    assert test.ep == 'g6'

def test_ep_g6_correctLA():
    test = Fen('4k3/8/8/5Pp1/8/8/8/4K3 w - g6 0 1')
    assert test.ep == 'g6'

def test_ep_g6_incorrect():
    test = Fen('4k3/8/8/P5p1/8/8/8/4K3 w - g6 0 1')
    assert test.ep == '-'

def test_ep_h6_correct():
    test = Fen('4k3/8/8/6Pp/8/8/8/4K3 w - h6 0 1')
    assert test.ep == 'h6'

def test_ep_h6_incorrect():
    test = Fen('4k3/8/8/1P5p/8/8/8/4K3 w - h6 0 1')
    assert test.ep == '-'

def test_ep_a3_correct():
    test = Fen('4k3/8/8/8/Pp6/8/8/4K3 b - a3 0 1')
    assert test.ep == 'a3'

def test_ep_a3_incorrect():
    test = Fen('4k3/8/8/8/P1p5/8/8/4K3 b - a3 0 1')
    assert test.ep == '-'

def test_ep_b3_correctRA():
    test = Fen('4k3/8/8/8/1Pp5/8/8/4K3 b - b3 0 1')
    assert test.ep == 'b3'

def test_ep_b3_correctLA():
    test = Fen('4k3/8/8/8/pP6/8/8/4K3 b - b3 0 1')
    assert test.ep == 'b3'

def test_ep_b3_incorrect():
    test = Fen('4k3/8/8/8/1P1p4/8/8/4K3 b - b3 0 1')
    assert test.ep == '-'

def test_ep_c3_correctRA():
    test = Fen('4k3/8/8/8/2Pp4/8/8/4K3 b - c3 0 1')
    assert test.ep == 'c3'

def test_ep_c3_correctLA():
    test = Fen('4k3/8/8/8/1pP5/8/8/4K3 b - c3 0 1')
    assert test.ep == 'c3'

def test_ep_c3_incorrect():
    test = Fen('4k3/8/8/8/2P1p3/8/8/4K3 b - c3 0 1')
    assert test.ep == '-'

def test_ep_d3_correctRA():
    test = Fen('4k3/8/8/8/3Pp3/8/8/4K3 b - d3 0 1')
    assert test.ep == 'd3'

def test_ep_d3_correctLA():
    test = Fen('4k3/8/8/8/2pP4/8/8/4K3 b - d3 0 1')
    assert test.ep == 'd3'

def test_ep_d3_incorrect():
    test = Fen('4k3/8/8/8/3P1p2/8/8/4K3 b - d3 0 1')
    assert test.ep == '-'

def test_ep_e3_correctRA():
    test = Fen('4k3/8/8/8/4Pp2/8/8/4K3 b - e3 0 1')
    assert test.ep == 'e3'

def test_ep_e3_correctLA():
    test = Fen('4k3/8/8/8/3pP3/8/8/4K3 b - e3 0 1')
    assert test.ep == 'e3'

def test_ep_e3_incorrect():
    test = Fen('4k3/8/8/8/4p1P1/8/8/4K3 b - e3 0 1')
    assert test.ep == '-'

def test_ep_f3_correctRA():
    test = Fen('4k3/8/8/8/5Pp1/8/8/4K3 b - f3 0 1')
    assert test.ep == 'f3'

def test_ep_f3_correctLA():
    test = Fen('4k3/8/8/8/4pP2/8/8/4K3 b - f3 0 1')
    assert test.ep == 'f3'

def test_ep_f3_incorrect():
    test = Fen('4k3/8/8/8/5P1p/8/8/4K3 b - f3 0 1')
    assert test.ep == '-'

def test_ep_g3_correctRA():
    test = Fen('4k3/8/8/8/6Pp/8/8/4K3 b - g3 0 1')
    assert test.ep == 'g3'

def test_ep_g3_correctLA():
    test = Fen('4k3/8/8/8/5pP1/8/8/4K3 b - g3 0 1')
    assert test.ep == 'g3'

def test_ep_g3_incorrect():
    test = Fen('4k3/8/8/8/p5P1/8/8/4K3 b - g3 0 1')
    assert test.ep == '-'

def test_ep_h3_correct():
    test = Fen('4k3/8/8/8/6pP/8/8/4K3 b - h3 0 1')
    assert test.ep == 'h3'

def test_ep_h3_incorrect():
    test = Fen('4k3/8/8/8/1p5P/8/8/4K3 b - h3 0 1')
    assert test.ep == '-'

# ---------------------------------------------------------- 49 tests: total 80

# -------------------- fen elements out of order ------------------- ----------
# valid toPlay, castling and ep should be recognised

def test_orderFenValidEP():
    test = Fen(fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR d6 w KQkq 0 3')
    assert test.board == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

# ------------------------------------------------------------ 1 test: total 81

# ------------------- board errors: kings -------------------------------------

def test_noWhiteKing():
    # this checks that the absence of a white king results in an error
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_manyWhiteKings():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBKKB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_noBlackKing():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_manyBlackKings():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbkkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

# ----------------------------------------------------------- 4 tests: total 85

# -------------------- castling: Board incorrect ------------------------------

def test_castling_KQkq_Passed(good_fen):
    test = Fen(good_fen)
    assert test.castling == 'KQkq'

def test_KQkq_Wht_K_Moved():
    test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1B1R w KQkq - 2 2')
    # after 1 e4 e5 2 Ke2
    # system should change castling automatically to 'kq'
    assert test.castling == 'kq'

def test_KQkq_Blk_K_Moved():
    test = Fen('rnbq1bnr/ppppkppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3')
    # after 1e4 e5 2 Nf3 Ke7
    # system should change castling automatically to 'KQ'
    assert test.castling == 'KQ'

def test_KQkq_Wht_KR_Moved():
    test = Fen('r1bqkbnr/pppp1ppp/2N5/4p3/4P3/8/PPPP1PPP/RNBQKBR1 w KQkq - 3 3')
    # after 1 e4 e5 2 Nf3 Nc6 3 Rg1
    # system should change castling automatically to 'Qkq'
    assert test.castling == 'Qkq'

def test_KQkq_Blk_KR_Moved():
    test = Fen('rnbqkbr1/pppp1ppp/5n2/4p3/4P3/2N2N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4')
    # after 1 e4 e5 2 Nf3 Nf6 3 Nc3 Rg8
    # system should change castling automatically to 'KQq'
    assert test.castling == 'KQq'

def test_KQkq_Both_KR_Moved():
    test = Fen('rnbqkbr1/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKBR1 w KQkq - 4 4')
    # after 1 e4 e5 2 Nf3 Nf6 3 Rg1 Rg8
    # system should change castling automatically to 'Qq'
    assert test.castling == 'Qq'

def test_KQkq_Wht_QR_Moved():
    test = Fen('r1bqkbnr/pppppppp/2N5/8/8/2N5/PPPPPPPP/1RBQKBNR b KQkq - 3 2')
    # after 1 Nc3 Nc6 2 Rb1
    # system should change castling automatically to 'Kkq'
    assert test.castling == 'Kkq'

def test_KQkq_Blk_QR_Moved():
    test = Fen('1rbqkbnr/pppppppp/2N5/8/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 3')
    # after 1 Nc3 Nc6 2 e4 Rb8
    # system should change castling automatically to 'KQk'
    assert test.castling == 'KQk'

def test_KQkq_Both_QR_Moved():
    test = Fen('1rbqkbnr/pppppppp/2N5/8/8/2N5/PPPPPPPP/1RBQKBNR b KQkq - 1 3')
    # after 1 Nc3 Nc6 2 Rb1 Rb8
    # system should change castling automatically to 'Kk'
    assert test.castling == 'Kk'

def test_KQk_Passed_position_unclear(): # Blk Rook moved and moved back
    test = Fen('r1bqkb1r/ppp2ppp/2np1n2/4p3/4P3/2NP1N2/PPP2PPP/R1BQKB1R w KQk -')
        # in this position it is not clear whether or not the Kings or Rooks
        # have moved as each Rook could have moved and moved back and the kings
        # could have moved and directly moved back or taken a triangluar
        # route back to their original square.
    assert test.castling == 'KQk'
        # program accepts input

#random selection of other possibilities

def test_KQq_Wht_K_Moved():
    test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1B1R w KQq - 2 2')
    # after 1 e4 e5 2 Ke2
    # system should change castling automatically to 'q' as passed value implies
    # q-side castling still Ok, but not so given Wnt K position
    assert test.castling == 'q'

def test_KQq_Wht_KR_Moved():
    test = Fen('r1bqkbnr/pppp1ppp/2N5/4p3/4P3/8/PPPP1PPP/RNBQKBR1 w KQq - 3 3')
    # after 1 e4 e5 2 Nf3 Nc6 3 Rg1
    # accepting the implied input that Blk KR moved and moved back the system
    # should change castling automatically to 'Qq'
    assert test.castling == 'Qq'

def test_KQk_Blk_K_Moved():
    test = Fen('rnbq1bnr/ppppkppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQk - 2 3')
    # after 1e4 e5 2 Nf3 Ke7
    # system should change agree to passed value 'KQ'
    assert test.castling == 'KQ'

def test_KQ_Blk_KR_Moved():
    test = Fen('rnbqkbr1/pppp1ppp/5n2/4p3/4P3/2N2N2/PPPP1PPP/RNBQKB1R w KQ - 4 4')
    # after 1 e4 e5 2 Nf3 Nf6 3 Nc3 Rg8
    # system should leave castling as 'KQ'
    assert test.castling == 'KQ'

def test_Kkq_Both_KR_Moved():
    test = Fen('rnbqkbr1/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKBR1 w Kkq - 4 4')
    # after 1 e4 e5 2 Nf3 Nf6 3 Rg1 Rg8
    # system should change castling automatically to 'q'
    assert test.castling == 'q'

def test_Qkq_Wht_QR_Moved():
    test = Fen('r1bqkbnr/pppppppp/2N5/8/8/2N5/PPPPPPPP/1RBQKBNR b Qkq - 3 2')
    # after 1 Nc3 Nc6 2 Rb1
    # system should change castling automatically to 'Kkq'
    assert test.castling == 'kq'

def test_Qkq_Blk_QR_Moved():
    test = Fen('1rbqkbnr/pppppppp/2N5/8/4P3/2N5/PPPP1PPP/R1BQKBNR b Qkq - 1 3')
    # after 1 Nc3 Nc6 2 e4 Rb8
    # system should change castling automatically to 'KQk'
    assert test.castling == 'Qk'

def test_Qkq_Both_QR_Moved():
    test = Fen('1rbqkbnr/pppppppp/2N5/8/8/2N5/PPPPPPPP/1RBQKBNR b Qkq - 1 3')
    # after 1 Nc3 Nc6 2 Rb1 Rb8
    # system should change castling automatically to 'Kk'
    assert test.castling == 'k'
# --------------------------------------------------------- 18 tests: total 103

# -------------------- test board display -------------------------------------

def test_boardDisplay():
    test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    y = test.boardToArray('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
    assert y == ['  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n',
        '  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n',
        '  .   .   .   .   .   .   .   .   \n',
        '  .   .   .   .   \x1b[31mp   \x1b[0m.   .   .   \n',
        '  .   .   .   .   P   .   .   .   \n',
        '  .   .   .   .   .   N   .   .   \n',
        '  P   P   P   P   .   P   P   P   \n',
        '  R   N   B   Q   K   B   .   R   \n']
    test.displayBoard(y)
    z = test.augmentBoard()
    assert z == ['\x1b[32m\n        a   b   c   d   e   f   g   h  \n\x1b[0m',
    '\x1b[32m  8   \x1b[0m  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n',
    '\x1b[32m  7   \x1b[0m  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n',
    '\x1b[32m  6   \x1b[0m  .   .   .   .   .   .   .   .   \n',
    '\x1b[32m  5   \x1b[0m  .   .   .   .   \x1b[31mp   \x1b[0m.   .   .   \n',
    '\x1b[32m  4   \x1b[0m  .   .   .   .   P   .   .   .   \n',
    '\x1b[32m  3   \x1b[0m  .   .   .   .   .   N   .   .   \n',
    '\x1b[32m  2   \x1b[0m  P   P   P   P   .   P   P   P   \n',
    '\x1b[32m  1   \x1b[0m  R   N   B   Q   K   B   .   R   \n']
    test.displayBoard(z)

def test_boardDisplayNotExplicit():
    test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    y = test.boardToArray('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
    assert y == ['  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n',
        '  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n',
        '  .   .   .   .   .   .   .   .   \n',
        '  .   .   .   .   \x1b[31mp   \x1b[0m.   .   .   \n',
        '  .   .   .   .   P   .   .   .   \n',
        '  .   .   .   .   .   N   .   .   \n',
        '  P   P   P   P   .   P   P   P   \n',
        '  R   N   B   Q   K   B   .   R   \n']
    test.displayBoard()
    z = test.augmentBoard()
    assert z == ['\x1b[32m\n        a   b   c   d   e   f   g   h  \n\x1b[0m',
    '\x1b[32m  8   \x1b[0m  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n',
    '\x1b[32m  7   \x1b[0m  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n',
    '\x1b[32m  6   \x1b[0m  .   .   .   .   .   .   .   .   \n',
    '\x1b[32m  5   \x1b[0m  .   .   .   .   \x1b[31mp   \x1b[0m.   .   .   \n',
    '\x1b[32m  4   \x1b[0m  .   .   .   .   P   .   .   .   \n',
    '\x1b[32m  3   \x1b[0m  .   .   .   .   .   N   .   .   \n',
    '\x1b[32m  2   \x1b[0m  P   P   P   P   .   P   P   P   \n',
    '\x1b[32m  1   \x1b[0m  R   N   B   Q   K   B   .   R   \n']
    test.displayBoard()

# ---------------------------------------------------------- 2 tests: total 105

# -------------------- too many pawns on board --------------------------------

def test_tooManyWhitePawns():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2P5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_tooManyBlackPawns():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4p3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # input of corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

# ---------------------------------------------------------- 2 tests: total 107
