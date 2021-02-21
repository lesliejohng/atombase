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

def test_missingFen():
    # full reset to starting position
    test = Fen()
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '0'
    assert test.fenElementDict.get('fenMoveCounter') == '1'

def test_nonStringFen():
    # temporary: full reset to starting position
    test = Fen(5)
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '0'
    assert test.fenElementDict.get('fenMoveCounter') == '1'

def test_insufficientFen():
    # temporary: fen Board is as given
    # temporary: other elements reset to those in the starting position
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '0'
    assert test.fenElementDict.get('fenMoveCounter') == '1'

def test_invalidCharInBoard():
    test = Fen('rnbqkbnr/pp1ppppp/8/2x5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_noWhiteKing():
    # this checks that the absence of a white king results in an error
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_manyWhiteKings():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_noBlackKing():
    test = Fen('rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_manyBlackKings():
    test = Fen('rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_toPlayError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    # temporary: reset fenTOPlay to 'w'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_CastlingError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    # temporary: reset fenCastling to 'KQkq'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPNone():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPNoToPlayElement():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R - KQkq e6 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    # temporary: reset fenToPlay to 'w'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == 'e6'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPInvalidSquare():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    # temporary: reset fenEP to '-'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPwtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == 'e6'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPbtpValid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == 'e3'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPwtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'w'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    # temporary: reset fenEP to '-'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_EPbtpInvalid():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    # temporary: reset fenEP to '-'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_validHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 5')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '3'
    assert test.fenElementDict.get('fenMoveCounter') == '5'

def test_invalidHalfMove():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - x 5')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    # temporary: reset half move to 0
    assert test.fenElementDict.get('fenHalfMoveClock') == '0'
    assert test.fenElementDict.get('fenMoveCounter') == '5'

def test_validMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

def test_invalidMoveCount():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 x')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    # temporary: reset fenMoveCounter to '1'
    assert test.fenElementDict.get('fenMoveCounter') == '1'

def test_noError():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.fenElementDict.get('fenBoard') == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.fenElementDict.get('fenToPlay') == 'b'
    assert test.fenElementDict.get('fenCastling') == 'KQkq'
    assert test.fenElementDict.get('fenEP') == '-'
    assert test.fenElementDict.get('fenHalfMoveClock') == '1'
    assert test.fenElementDict.get('fenMoveCounter') == '2'

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

def test_goodBoardDiaplay(good_fen):
    x = good_fen.fenElementDict.get('fenBoard')
    y = good_fen.boardToArray(x)
    z = good_fen.augmentBoard(y)
    assert y == ['  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n', '  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n', '  .   .   .   .   .   .   .   .   \n', '  .   .   \x1b[31mp   \x1b[0m.   .   .   .   .   \n', '  .   .   .   .   P   .   .   .   \n', '  .   .   .   .   .   N   .   .   \n', '  P   P   P   P   .   P   P   P   \n', '  R   N   B   Q   K   B   .   R   \n']
    assert z == ['\x1b[32m\n        a   b   c   d   e   f   g   h  \n\x1b[0m', '\x1b[32m  8   \x1b[0m  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mr   \x1b[0m\n', '\x1b[32m  7   \x1b[0m  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n', '\x1b[32m  6   \x1b[0m  .   .   .   .   .   .   .   .   \n', '\x1b[32m  5   \x1b[0m  .   .   \x1b[31mp   \x1b[0m.   .   .   .   .   \n', '\x1b[32m  4   \x1b[0m  .   .   .   .   P   .   .   .   \n', '\x1b[32m  3   \x1b[0m  .   .   .   .   .   N   .   .   \n', '\x1b[32m  2   \x1b[0m  P   P   P   P   .   P   P   P   \n', '\x1b[32m  1   \x1b[0m  R   N   B   Q   K   B   .   R   \n']

def test_boardDisplayBadChar():
    test = Fen()
    y = test.boardToArray('rnbqkbxr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R')
    z = test.augmentBoard(y)
    assert y == ['  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m?   \x1b[31mr   \x1b[0m\n', '  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n', '  .   .   .   .   .   .   .   .   \n', '  .   .   \x1b[31mp   \x1b[0m.   .   .   .   .   \n', '  .   .   .   .   P   .   .   .   \n', '  .   .   .   .   .   N   .   .   \n', '  P   P   P   P   .   P   P   P   \n', '  R   N   B   Q   K   B   .   R   \n']
    assert z == ['\x1b[32m\n        a   b   c   d   e   f   g   h  \n\x1b[0m', '\x1b[32m  8   \x1b[0m  \x1b[31mr   \x1b[0m\x1b[31mn   \x1b[0m\x1b[31mb   \x1b[0m\x1b[31mq   \x1b[0m\x1b[31mk   \x1b[0m\x1b[31mb   \x1b[0m?   \x1b[31mr   \x1b[0m\n', '\x1b[32m  7   \x1b[0m  \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m.   \x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\x1b[31mp   \x1b[0m\n', '\x1b[32m  6   \x1b[0m  .   .   .   .   .   .   .   .   \n', '\x1b[32m  5   \x1b[0m  .   .   \x1b[31mp   \x1b[0m.   .   .   .   .   \n', '\x1b[32m  4   \x1b[0m  .   .   .   .   P   .   .   .   \n', '\x1b[32m  3   \x1b[0m  .   .   .   .   .   N   .   .   \n', '\x1b[32m  2   \x1b[0m  P   P   P   P   .   P   P   P   \n', '\x1b[32m  1   \x1b[0m  R   N   B   Q   K   B   .   R   \n']

def test_toPlayInput():
    test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R x KQkq - 1 2')
