from fenChecker import Fen, WarningMsg

test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
# arguments given
x = test.boardToArray('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
test.displayBoard(x)
y = test.augmentBoard(x)
test.displayBoard(y)
