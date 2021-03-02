import pytest
from fenChecker import Fen, WarningMsg
import mock

startingFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# manual count of tests = 6

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
    return Fen('rnbqkbnr/pppp1ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR # w KQkq e3 0 3')

# -----------------------------------------------------------------------------

# -------------------- tests: non-string fen (4) ------------------------------

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

# -----------------------------------------------------------------------------

# -------------------- test sub-string assumptions (1) ------------------------

# In handling a string input I have made the following assumptions
#       1) the first sub-string is always the board
#       2) the last sub-string is always the move counter IF A DIGIT
#       3) the penultimate sub-string is always the half move clock IF A DIGIT
#          AND the last sub-string is ALSO A DIGIT

def test_noBoardSubstring():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R',
    'w','KQkq','-']): # half move and move accepted and not reset
        test = Fen(fen = 'w KQkq - 1 2')
        # no board element passed
        # only the last two items accepted
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        # fenToPlay set to test default 'w'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'

# -------------------- fen passed with missing elements (1) -------------------
# NB this depends on my assumptions that
#       1) the first sub-string is always the board
#       2) the last sub-string is always the move counter IF A DIGIT
#       3) the preultimate sub-string is always the half move clock IF A DIGIT

def test_insufficientFen():
    with mock.patch('builtins.input',side_effect = ['w','KQkq','-']): # full reset to starting position
        test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
        # reset all but board, as missing element requires input of all
        # other elements of the fen
        assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        # fenToPlay set to test default 'w'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '1'
        assert test.move == '2'
        assert str(test) == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'
