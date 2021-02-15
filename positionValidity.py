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

    def __init__(self, fen ='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):

        # Variables required for checking fen elements
            # A) castling
        self.validCastling =['-','q','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kkq','Kq','Kk','Kkq','KQ','KQq','KQk',
                   'KQkq']
            # B) valid EP square
        self.validEPwtp = ['a6','b6','c6','d6','e6','f6','g6','h6']
        self.validEPbtp = ['a3','b3','c3','d3','e3','f3','g3','h3']
        self.validEPsquares = self.validEPwtp + self.validEPbtp

        # required
        self.fenElementDict = {}

        # initial processing
        if isinstance(fen, str):
            self.fen = fen
            self.fenElements = fen.split(' ')
            self.fenElementDict['fenBoard']= self.fenElements[0]

            if len(self.fenElements) == 6:
                if self.identifyToPlay(self.fenElements[1]):
                    self.fenElementDict['fenToPlay'] = self.fenElements[1]

                if self.identifyCastling(self.fenElements[2]):
                    self.fenElementDict['fenCastling'] = self.fenElements[2]

                if self.testEP(self.fenElements[3]):
                    self.fenElementDict['fenEP'] = self.fenElements[3]

                if self.fenElements[4].isdigit():
                    self.fenElementDict['fenHalfMoveClock'] = self.fenElements[4]
                else:
                    # as uncritical reset to 0
                    self.fenElementDict['fenHalfMoveClock'] = '0'

                if self.fenElements[5].isdigit():
                    self.fenElementDict['fenMoveCounter'] = self.fenElements[5]
                else:
                    # as uncritical reset to 1
                    self.fenElementDict['fenMoveCounter'] = '1'
            else:
                self.message = WarningMsg(header = 'Fen Error',
                    body = 'incomplete fen string',
                    instruction = 'please check fen has all the required elements')
                self.message
                self.partFenInput()

        else:
            self.message = WarningMsg(header = 'Fen Error',
                    body = 'input is not a string',
                    instruction = 'please re-input')
            self.message
            self.fullFenInput()

        self.testBoard()

    def __repr__(self):
        return self.fen

    # This section is for routines which identify fenElements

    def identifyToPlay(self, fenToPlay):
        # ToPlay consists of a single 'w' or 'b' character
        if fenToPlay == 'w' or fenToPlay == 'b':
            return True
        else:
            self.message = WarningMsg(header = 'Error in To Play element of fen',
                    body = str(fenToPlay)+' input is not valid',
                    instruction = 'should be either "w" or "b". Please re-input.')
            self.message
            self.toPlayInput()
            return True

    def identifyCastling(self,fenCastling):
        if not 'fenToPlay' in self.fenElementDict.keys():
            self.toPlayInput()

        if fenCastling in self.validCastling:
            return True
        else:
            self.message = WarningMsg(header = 'Castling: '+str(fenCastling),
                    body = 'The Castling Element is not in a valid form',
                    instruction = 'format "-" or up to 4 letters in order KQkq')
            self.message
            self.castlingInput()
            return False

    # This section is for input routines

    def partFenInput(self):
        # case of incomplete fen
        # temporary
        # sets all but fenBoard as if it ws the starting position
        self.fenElementDict['fenToPlay'] = 'w'
        self.fenElementDict['fenCastling'] = 'KQkq'
        self.fenElementDict['fenEP'] = '-'
        self.fenElementDict['fenHalfMoveClock'] = '0'
        self.fenElementDict['fenMoveCounter'] = '1'

    def fullFenInput(self):
        # temporary
        # set these values
        self.fenElementDict['fenBoard'] = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.fenElementDict['fenToPlay'] = 'w'
        self.fenElementDict['fenCastling'] = 'KQkq'
        self.fenElementDict['fenEP'] = '-'
        self.fenElementDict['fenHalfMoveClock'] = '0'
        self.fenElementDict['fenMoveCounter'] = '1'

    def toPlayInput(self):
        # temporary
        # set ToPlay to white
        self.fenElementDict['fenToPlay'] = 'w'

    def castlingInput(self):
        # temporary
        # set castling to call
        self.fenElementDict['fenCastling'] = 'KQkq'

    # This section is for deeper validity checks
    def testBoard(self):
        # this is a series of tests on the board to see if it valid

        # test that there are two kings on the fenBoard
        # one White and one Black
        self.whiteKing = self.fenElementDict['fenBoard'].count('K')
        self.blackKing = self.fenElementDict['fenBoard'].count('k')

        if self.whiteKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no White King on the board')
            self.message

        if self.whiteKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many White Kings on the Board')
            self.message

        if self.blackKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no Black King on the board')
            self.message

        if self.blackKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many Black Kings on the board')
            self.message

    def testEP(self,fenEP):
        if fenEP == '-' or len(fenEP) == 2:

            if fenEP == '-':
                return True
            else:
                if fenEP in self.validEPsquares:
                    if self.fenElementDict.get('fenToPlay') == 'w':
                        if fenEP in self.validEPwtp:
                            return True
                        else:
                            self.message = WarningMsg(header = 'EP square: ' + str(fenEP),
                                body = 'The EP square is not valid in a "white to play" position')
                            self.message
                            return False

                    if self.fenElementDict.get('fenToPlay') == 'b':
                        if fenEP in self.validEPbtp:
                            return True
                        else:
                            self.message = WarningMsg(header = 'EP square' + str(fenEP),
                                body = 'The EP square is not valid in a "black to play" position')
                            self.message
                            return False
                else:
                    self.message = WarningMsg(header = 'EP '+ str(fenEP),
                        body = 'The EP Element is not a valid square')
                    self.message
                    return False

                if self.fenElementDict.get('fenToPlay' ,'unknown') == 'unknown':
                    self.message = WarningMsg(header = 'EP square ' + str(fenEP),
                        body = 'It is not known who it is to play',
                        instruction = 'It is not possible to check the validity of the EP square')
                    self.message
                    return False

        else:
            self.message = WarningMsg(header = '"EP" element of fen',
                body = 'This element is too long')
            self.message
            return False

# initial test
# test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
# print(test.fenElementDict.get('fenEP', 'unknown'))
















#
