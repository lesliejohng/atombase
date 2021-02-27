from fenChecker import Fen, WarningMsg

# initial test
print('****************************************************************')
print('test all castling OK')
fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
board = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
test = Fen(fen)
a = test.boardToString(board=board)
print(a)
print(len(a))
boardString = test.boardToString(board)
b = test.interrogateBoard(boardString = boardString, targetSquare = 'e8')
print('The piece on e8 is a ' + b)
c = test.checkCastling(board =board, castling = 'KQkq')
print('castling passed "KQkq" : ' + c)
c = test.checkCastling(board =board, castling = '-')
print('castling passed "-" : ' + c)
c = test.checkCastling(board =board, castling = 'kq')
print('castling passed "kq" : ' + c)
c = test.checkCastling(board =board, castling = '')
print('castling nothing passed: ' + c)
c = test.checkCastling(board =board, castling = "?")
print('castling question mark element passed: ' + c)

print('****************************************************************')
print('test Black King moved')
fen = 'rnbkqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
board = 'rnbkqbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
test = Fen(fen)
a = test.boardToString(board=board)
print(a)
print(len(a))
boardString = test.boardToString(board)
b = test.interrogateBoard(boardString = boardString, targetSquare = 'e8')
print('The piece on e8 is a ' + b)
c = test.checkCastling(board =board, castling = 'KQkq')
print('castling passed "KQkq" : ' + c)
c = test.checkCastling(board =board, castling = '-')
print('castling passed "-" : ' + c)
c = test.checkCastling(board =board, castling = 'kq')
print('castling passed "kq" : ' + c)
c = test.checkCastling(board =board, castling = "?")
print('castling question mark element passed: ' + c)

print('****************************************************************')
print('test Wht QR moved')
fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/1NBQKB1R b KQkq - 1 2'
board = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/1NBQKB1R'
test = Fen(fen)
a = test.boardToString(board=board)
print(a)
print(len(a))
boardString = test.boardToString(board)
b = test.interrogateBoard(boardString = boardString, targetSquare = 'e8')
print('The piece on e8 is a ' + b)
c = test.checkCastling(board =board, castling = 'KQkq')
print('castling passed "KQkq" : ' + c)
c = test.checkCastling(board =board, castling = '-')
print('castling passed "-" : ' + c)
c = test.checkCastling(board =board, castling = 'kq')
print('castling passed "kq" : ' + c)
c = test.checkCastling(board =board, castling = "?")
print('castling question mark element passed: ' + c)

print('****************************************************************')
print('test Wht K moved and moved back')
fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
board = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
test = Fen(fen)
a = test.boardToString(board=board)
print(a)
print(len(a))
boardString = test.boardToString(board)
b = test.interrogateBoard(boardString = boardString, targetSquare = 'e8')
print('The piece on e8 is a ' + b)
c = test.checkCastling(board =board, castling = 'kq')
print('castling passed "kq" to show white K moved and moved back: ' + c)

print('****************************************************************')





#
