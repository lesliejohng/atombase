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
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR KQkq d6 0 3')
        # the missing toPlay would make it impossible to check ep,
        # but toPlay should be set in time to prevent  problem
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingCastling():
    with mock.patch('builtins.input',side_effect = ['KQkq']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w d6 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingEP():
    with mock.patch('builtins.input',side_effect = ['d6']):
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenMissingDigit():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 3')
    # assumed that the provided digit is the move number
    # half move will be reset to 0
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

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

def test_castling_None():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    assert test.ep == 'e3'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_castling_ep_None():
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

def test_2Blanks_ep_None():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b - -  e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == '-'
    assert test.ep == 'e3'
    assert test.halfMove == '1'
    assert test.move == '2'

# ----------------------------------------------------------- 5 tests: total 20

# -------------------- test of extra white spaces -----------------------------

def test_fenWhiteSpaceBetweenElements():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR  w     KQkq d6 0  3')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenLeadingWhiteSapce():
    test = Fen(fen = '        rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0  3')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenTrailingWhiteSpace():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR  w KQkq d6 0 3     ')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

def test_fenWhiteSpaceInBoard():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR']):
        # will require re-input of board
        test = Fen(fen = 'rnbqkbnr/pp1pppp p/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3')
        assert test.board == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == 'd6'
        assert test.halfMove == '0'
        assert test.move == '3'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/8/3Pp3/4p3/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

# -----------------------------------------------------------   1 test: total 21

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

# -----------------------------------------------------------------------------

# -------------------- ep invalid squares (tests 5: total 22) -----------------

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
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'e6'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_epbtpValid():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == 'e3'
    assert test.halfMove == '1'
    assert test.move == '2'

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

# -----------------------------------------------------------------------------

# -------------------- fen elements out of order (tests 1: total 23) ----------
# valid toPlay, castling and ep should be recognised

def test_orderFenValidEP():
    test = Fen(fen = 'rnbqkbnr/pppp1ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR d6 w KQkq 0 3')
    assert test.board == 'rnbqkbnr/pppp1ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'd6'
    assert test.halfMove == '0'
    assert test.move == '3'
    assert str(test) == 'rnbqkbnr/pppp1ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3'

# ------------------- board errors: kings (tests 4 : total 27)-----------------

def test_noWhiteKing():
    # this checks that the absence of a white king results in an error
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
        # input fo corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_manyWhiteKings():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBKKB1R b KQkq - 1 2')
        # input fo corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_noBlackKing():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # input fo corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

def test_manyBlackKings():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq']): # full reset to starting position
        test = Fen(fen = 'rnbkkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
        # input fo corrected board element
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq'
        assert test.toPlay == 'b'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'

# -------------------- test board display (2 test: total 29) ------------------

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
# -----------------------------------------------------------------------------
