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
                            'w','KQkq','-','0','1']):# full reset to starting position
        assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        assert test.toPlay == 'w'
        assert test.castling == 'KQkq'
        assert test.ep == '-'
        assert test.halfMove == '0'
        assert test.move == '1'
        assert test == startingFen

def test_nonStringFen():
    test = Fen( fen=5)
    # full reset to starting position
    # this is achieved withing the class Fen, so requires a full List
    # of tested elements
    assert test.board == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    # fenToPlay set to test default 'w'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '0'
    assert test.move == '1'

def test_insufficientFen():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R KQkq - 1 2')
    # reset all but board, as missing element requires input of all
    # other elements of the fen
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    # fenToPlay set to test default 'w'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '0'
    assert test.move == '1'

def test_invalidCharInBoard():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2x5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_noWhiteKing():
    # this checks that the absence of a white king results in an error
    test = Fen(fen ='rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQQB1R'
    assert test.toPlay == 'b'
    # no white king
    assert test.castling == 'kq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_manyWhiteKings():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKK1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_noBlackKing():
    test = Fen(fen = 'rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.board == 'rnbqqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    #no black king
    assert test.castling == 'KQ'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_manyBlackKings():
    test = Fen(fen = 'rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # temporary: reset board to starting position
    assert test.board == 'rnbqkknr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_toPlayError():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R z KQkq - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    # fenToPlay set to test default 'w'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'
    caseWhite = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 1 2'
    caseBlack = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
    assert test.fenReconstruct() == caseWhite
    test.fenElementDict['fenToPlay'] = 'b'
    assert test.fenReconstruct() == caseBlack

def test_CastlingError():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkx - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    # temporary: reset fenCastling to 'KQkq'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_ep_None():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_toPlay_NoToPlayElement():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R - KQkq e6 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    # fenToPlay reset to test default 'w'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    # as fenToPlay reset to 'w', e6 is valid
    assert test.ep == 'e6'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_test.epInvalidSquare():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e5 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    # temporary: reset fentest.ep to '-'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_test.epwtpValid():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e6 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    assert test.ep == 'e6'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_epbtpValid():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e3 1 2')
    assert test.fenElementDict.get('fenBoard', 'unknown') != 'unknown'
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == 'e3'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_epwtpInvalid():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'w'
    assert test.castling == 'KQkq'
    # temporary: reset fentest.ep to '-'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_epbtpInvalid():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq e6 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    # temporary: reset fentest.ep to '-'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_validtest.halfMove():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 3 5')
    # test.halfMove is a digit, so no test
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '3'
    assert test.move == '5'

def test_invalidtest.halfMove():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - x 5')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    # reset half move to 0
    assert test.halfMove == '0'
    assert test.move == '5'

def test_validMoveCount():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    # move is a digit so there is no test
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_invalidMoveCount():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 x')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    # reset fenMoveCounter to '1'
    assert test.move == '1'

def test_noError():
    test = Fen(fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
    assert test.board == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert test.toPlay == 'b'
    assert test.castling == 'KQkq'
    assert test.ep == '-'
    assert test.halfMove == '1'
    assert test.move == '2'

def test_fenElements(good_fen):
    assert len(good_fen.fenElements) == 6
    assert good_fen.board ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert good_fen.toPlay == 'b'
    assert good_fen.castling == 'KQkq'
    assert good_fen.fenElementDict.get('fentest.ep') == '-'
    assert good_fen.fenElementDict.get('fentest.eptest.halfMove') == '1'
    assert good_fen.fenElementDict.get('fenMove') == '2'

def test_fenElements(good_test.ep_fen):
    assert len(good_test.ep_fen.fenElements) == 6
    assert good_test.ep_fen.board ==  'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
    assert good_test.ep_fen.toPlay == 'b'
    assert good_test.ep_fen.castling == 'KQkq'
    assert good_test.ep_fen.fenElementDict.get('fentest.ep') == 'e3'
    assert good_test.ep_fen.fenElementDict.get('fentest.halfMove') == '1'
    assert good_test.ep_fen.fenElementDict.get('fenMove') == '2'

def test_goodBoardDiaplay(good_fen):
    x = good_fen.board
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

def test_toPlayInputw():
    with mock.patch('builtins.input',return_value = "w"):
        assert Fen.toPlayInput() == "w"

def test_toPlayInputb():
    with mock.patch('builtins.input',return_value = "b"):
        assert Fen.toPlayInput() == "b"

def test_toPlayIncorrectInput():
    with mock.patch('builtins.input',side_effect = ["K","w"]):
        assert Fen.toPlayInput() == "w"
