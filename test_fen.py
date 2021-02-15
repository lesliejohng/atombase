import pytest
from positionValidity import WarningMsg, Fen

@pytest.fixture
def good_fen():
    # sets up a Fen object with a valid fen
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

@pytest.fixture
def good_ep_fen():
    # sets up a Fen object with a valid EP square
    return Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')

def test_insufficient_fen():
    # this makes sure that I have not added anything to the program
    # which breaks my rules that
    #   1 The fenBoard element should never be set to 'unknown'
    #   2 A problem with the fenHalfMoveClock element should just result
    #       in the value being reset to 0
    #   3 A problem with the fenHalfMoveClock element should just result
    #       in the value being reset to 0
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
    assert test.errorLog == ['fenError']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_noWhiteKing():
    # this checks that the absence of a white king results in an error
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    assert test.errorLog == ['noWhiteKing']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_manyWhiteKings():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R b KQkq - 1 2')
    assert test.errorLog == ['manyWhiteKings']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_noBlackKing():
    test = Fen('rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['noBlackKing']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_manyBlackKings():
    test = Fen('rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == ['manyBlackKings']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_toPlayError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
    assert test.errorLog == ['fenToPlayError']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_toPlayLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R bb KQkq - 1 2')
    assert test.errorLog == ['fenToPlayLength']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_CastlingCharacters():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
    assert test.errorLog == ['fenCastlingError']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_CastlingOrder():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQqk - 1 2')
    assert test.errorLog == ['fenCastlingError']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_CastlingLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkqx - 1 2')
    assert test.errorLog == ['fenCastlingLength']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPLength():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq ee6 1 2')
    assert test.errorLog == ['fenEPLength']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPNone():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPUnknown():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R - KQkq e6 1 2')
    assert test.errorLog == ['fenToPlayError', 'fenEPSquareUnclear']
    assert test.fenElementDict.get('fenBoard', 'unknown')!= 'unknown'
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPInvalidSquare():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPwtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPbtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPwtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_EPbtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
    assert test.errorLog == ['fenEPSquareInvalid']
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_validHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 5')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock') == '3'
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_invalidHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - x 5')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock') == '0'
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_validMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_invalidMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 x')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter') == '1'

def test_noError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.errorLog == []
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenHalfMoveClock').isdigit()
    assert test.fenElementDict.get('fenMoveCounter').isdigit()

def test_fenElements(good_fen):
    assert len(good_fen.fenElements) == 6
    assert good_fen.fenElementDict.get('fenBoard') ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert good_fen.fenElementDict.get('fenToPlay') == 'b'
    assert good_fen.fenElementDict.get('fenCastling') == 'KQkq'
    assert good_fen.fenElementDict.get('fenEP') == '-'
    assert good_fen.fenElementDict.get('fenEPHalfMoveClock') == '1'
    assert good_fen.fenElementDict.get('fenMoveCounter') == '2'

def test_fenElements(good_ep_fen):
    assert len(good_ep_fen.fenElements) == 6
    assert good_ep_fen.fenElementDict.get('fenBoard') ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert good_ep_fen.fenElementDict.get('fenToPlay') == 'b'
    assert good_ep_fen.fenElementDict.get('fenCastling') == 'KQkq'
    assert good_ep_fen.fenElementDict.get('fenEP') == 'e3'
    assert good_ep_fen.fenElementDict.get('fenHalfMoveClock') == '1'
    assert good_ep_fen.fenElementDict.get('fenMoveCounter') == '2'
