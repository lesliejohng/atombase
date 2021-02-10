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

def test_toPlayError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
    assert test.errorLog == ['fenToPlayError']

def test_toPlayLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R bb KQkq - 1 2')
    assert test.errorLog == ['fenToPlayLength']

def test_CastlingCharacters():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
    assert test.errorLog == ['fenCastlingError']

def test_CastlingOrder():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQqk - 1 2')
    assert test.errorLog == ['fenCastlingError']

def test_CastlingLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkqx - 1 2')
    assert test.errorLog == ['fenCastlingLength']

def test_EPLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ee6 1 2')
    assert test.errorLog == ['fenEPLength']

def test_EPNone():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []

def test_EPUnknown():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R - KQkq e6 1 2')
    assert test.errorLog == ['fenToPlayError', 'fenEPSquareUnclear']

def test_EPInvalidSquare():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']

def test_EPwtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.errorLog == []

def test_EPbtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.errorLog == []

def test_EPwtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']

def test_EPbtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']

def test_validHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 5')
    assert test.fenHalfMoveClock == '3'

def test_invalidHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - x 5')
    assert test.fenHalfMoveClock == '0'

def test_validMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.fenMoveCounter == '2'

def test_invalidMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 x')
    assert test.fenMoveCounter == '1'

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
