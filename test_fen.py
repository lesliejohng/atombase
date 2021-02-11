import pytest
from positionValidity import WarningMsg, Fen

@pytest.fixture
def good_fen():
    # sets up a Fen object with a valid fen
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

def test_insufficient_fen():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
    assert test.errorLog == ['fenError']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_noWhiteKing():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    assert test.errorLog == ['noWhiteKing']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_manyWhiteKings():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R b KQkq - 1 2')
    assert test.errorLog == ['manyWhiteKings']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_noBlackKing():
    test = Fen('rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['noBlackKing']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_manyBlackKings():
    test = Fen('rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['manyBlackKings']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_toPlayError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
    assert test.errorLog == ['fenToPlayError']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_toPlayLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R bb KQkq - 1 2')
    assert test.errorLog == ['fenToPlayLength']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_CastlingCharacters():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
    assert test.errorLog == ['fenCastlingError']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_CastlingOrder():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQqk - 1 2')
    assert test.errorLog == ['fenCastlingError']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_CastlingLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkqx - 1 2')
    assert test.errorLog == ['fenCastlingLength']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ee6 1 2')
    assert test.errorLog == ['fenEPLength']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPNone():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPUnknown():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R - KQkq e6 1 2')
    assert test.errorLog == ['fenToPlayError', 'fenEPSquareUnclear']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPInvalidSquare():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPwtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.errorLog == []
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPbtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.errorLog == []
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPwtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_EPbtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_validHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 5')
    assert test.fenHalfMoveClock == '3'
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_invalidHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - x 5')
    assert test.fenHalfMoveClock == '0'
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_validMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.fenMoveCounter == '2'
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_invalidMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 x')
    assert test.fenMoveCounter == '1'
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_noError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []
    assert test.fenBoard != 'unknown'
    assert test.fenHalfMoveClock.isdigit()
    assert test.fenMoveCounter.isdigit()

def test_fenElements(good_fen):
    assert len(good_fen.fenElements) == 6
    assert good_fen.fenBoard ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert good_fen.fenToPlay == 'b'
    assert good_fen.fenCastling == 'KQkq'
    assert good_fen.fenEP == '-'
    assert good_fen.fenHalfMoveClock == '1'
    assert good_fen.fenMoveCounter == '2'
