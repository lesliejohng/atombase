import pytest
from fenChecker import Fen, WarningMsg
import mock

startingFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

@pytest.fixture
def good_fen():
    # sets up a Fen object with a valid fen
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

@pytest.fixture
def good_ep_fen():
    # sets up a Fen object with a valid test.ep square
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R # BUG:  KQkq e3 1 2')

def test_missingFen():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # full reset to starting position
        # currently this is not an automatic reset to the starting position
        # as in pychess, but requires manual input of each element
        # of the fen
        test = Fen()
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen

def test_nonStringFen():
    with mock.patch('builtins.input',side_effect = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                            'w','KQkq','-']): # full reset to starting position
        test = Fen(fen = 5)
        # 5 is a valid fen character, so the board element consists of 5
        # blank squares
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert str(test) == startingFen
