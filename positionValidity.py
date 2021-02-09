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
        if len(self.fenElements) == 6:
            self.fenToPlay = self.fenElements[1]
            self.fenCastling = self.fenElements[2]
            self.fenEP = self.fenElements[3]
            self.fenHalfMoveClock = self.fenElements[4]
            self.fenMoveCounter = self.fenElements[5]

            self.testBoard()

        else:
            self.message = WarningMsg(header = 'Fen Error',
                body = 'incomplete fen string',
                instruction = 'please check fen has all the required elements')
            self.errorLog.append('fenError')
            self.message

            self.fenToPlay = 'unknown'
            self.fenCastling = 'unknown'
            self.fenEP = 'unknown'
            self.fenHalfMoveClock = 'unknown'
            self.fenMoveCounter = 'unknown'


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
















#
