# approach
# create fen class
# define the representation of the class as a fen string
# build into the fen class self checks about validity of the chess
# position represented in the initial fen string
# if possible the class will correct any errors in the initial fen
# before outputting a valid string

class WarningMsg():
    def __init__(self,
                    header = "Warning",
                    body = "Add your warning here",
                    instruction = "",
                    asterixNo = 60):
        self.header = header
        self.body = body
        self.instruction = instruction
        self.asterixNo = asterixNo
        self.printMessage()

    def dline(self):
        print('*' * self.asterixNo)

    def printMessage(self):
        self.dline()
        print("\n     "+self.header+"\n")
        print("\n     "+self.body+"\n")
        if self.instruction:
            print("\n     "+self.instruction+"\n")
        self.dline()


class Fen():
    def __init__(self, fen):
        self.fen = fen
        self.fenElements = fen.split(' ')
        self.fenBoard = self.fenElements[0]
        self.errorLog = []
        self.validCastling =['-','q','kq','Q','Qq','Qk','Qkq','K',
                    'Kq','Kkq','Kq','Kk','Kkq','KQ','KQq','KQk',
                    'KQkq']

        if len(self.fenElements) == 6:
            if self.testToPlay(self.fenElements[1]):
                self.fenToPlay = self.fenElements[1]
            else:
                self.fenToPlay = 'unknown'

            if self.testCastling(self.fenElements[2]):
                self.fenCastling = self.fenElements[2]
            else:
                self.fenCastling = 'unknown'

            self.fenEP = self.fenElements[3]
            self.fenHalfMoveClock = self.fenElements[4]
            self.fenMoveCounter = self.fenElements[5]
        else:
            self.fenToPlay = 'unknown'
            self.fenCastling = 'unknown'
            self.fenEP = 'unkown'
            self.fenHalfMoveClock = 'unknown'
            self.fenMoveCounter = 'unknown'

            self.message = WarningMsg(header = 'Fen Error',
                body = 'incomplete fen string',
                instruction = 'please check fen has all the required elements')
            self.errorLog.append('fenError')
            self.message

        self.testBoard()

        def __repr__(self):
         return self.fen

    def testBoard(self):
    # this is a series of tests on the board to see if it valid

    # test that there are two kings on the fenBoard
    # one White and one Black
        self.whiteKing = self.fenBoard.count('K')
        self.blackKing = self.fenBoard.count('k')

        if self.whiteKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no White King on the board')
            self.errorLog.append('noWhiteKing')
            self.message

        if self.whiteKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many White Kings on the Board')
            self.errorLog.append('manyWhiteKings')
            self.message

        if self.blackKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no Black King on the board')
            self.errorLog.append('noBlackKing')
            self.message

        if self.blackKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many Black Kings on the board')
            self.errorLog.append('manyBlackKings')
            self.message

    def testToPlay(self,fenToPlay):
        if len(fenToPlay) == 1:
            if fenToPlay in 'wb':
                return True
            else:
                self.message = WarningMsg(header = 'Insufficient Information',
                    body = 'Not clear whether it is White or Black to play',
                    instruction = 'format lowercase "w" or "b"')
                self.errorLog.append('fenToPlayError')
                self.message
                return False
        else:
            self.message = WarningMsg(header = '"To Play" element of fen',
                    body = 'This element is too long')
            self.errorLog.append('fenToPlayLength')
            self.message
            return False

    def testCastling(self,fenCastling):
        if len(fenCastling) < 5:
            if fenCastling in self.validCastling:
                return True
            else:
                self.message = WarningMsg(header = 'Castling',
                    body = 'The Castling Element is not in a valid form',
                    instruction = 'format "-" or up to 4 letters in order KQkq')
                self.errorLog.append('fenCastlingError')
                self.message
                return False
        else:
            self.message = WarningMsg(header = '"Castling" element of fen',
                body = 'This element is too long')
            self.errorLog.append('fenCastlingLength')
            self.message
            return False

#initial test
#test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
#print(test.errorLog)















#
