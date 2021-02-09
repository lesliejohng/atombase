import pytest
from positionValidity import WarningMsg, Fen

@pytest.fixture
def good_fen():
    # sets up a Fen object with a valid fen
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

def test_insufficient_fen():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
    assert test.errorLog == ['fenError']

def test_noWhiteKing():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    assert test.errorLog == ['noWhiteKing']

def test_manyWhiteKings():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R b KQkq - 1 2')
    assert test.errorLog == ['manyWhiteKings']

def test_noBlackKing():
    test = Fen('rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['noBlackKing']

def test_manyBlackKings():
    test = Fen('rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['manyBlackKings']

def test_noError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []

def test_fenElements(good_fen):
    assert len(good_fen.fenElements) == 6

def test_fenBoard(good_fen):
    assert good_fen.fenBoard ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'

def test_fenToPlay(good_fen):
    assert good_fen.fenToPlay == 'b'

def test_fenCastling(good_fen):
    assert good_fen.fenCastling == 'KQkq'

def test_fenEP(good_fen):
    assert good_fen.fenEP == '-'

def test_fenHalfMoveClock(good_fen):
    assert good_fen.fenHalfMoveClock == '1'

def test_fenMoveCounter(good_fen):
    assert good_fen.fenMoveCounter == '2'
