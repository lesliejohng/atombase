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

        # temporary to be removed upon completion of re-write
        self.errorLog = []

        # initial processing
        self.fen = fen
        self.fenElements = fen.split(' ')
        self.fenElementDict = {}
        self.fenElementDict['fenBoard']= self.fenElements[0]

    #def __init__(self, fen ='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    #    self.fen = fen
    #    self.fenElements = fen.split(' ')
    #    self.fenBoard =self.fenElements[0]
    #    self.errorLog = []
    #    self.validCastling =['-','q','kq','Q','Qq','Qk','Qkq','K',
    #                'Kq','Kkq','Kq','Kk','Kkq','KQ','KQq','KQk',
    #                'KQkq']
    #    self.validEPwtp = ['a6','b6','c6','d6','e6','f6','g6','h6']
    #    self.validEPbtp = ['a3','b3','c3','d3','e3','f3','g3','h3']
    #    self.validEPsquares = self.validEPwtp + self.validEPbtp

        if len(self.fenElements) == 6:
            if self.testToPlay(self.fenElements[1]):
                self.fenElementDict['fenToPlay'] = self.fenElements[1]
            #else:
                #self.fenToPlay = 'unknown'

            if self.testCastling(self.fenElements[2]):
                self.fenElementDict['fenCastling'] = self.fenElements[2]
            #else:
                #self.fenCastling = 'unknown'

            if self.testEP(self.fenElements[3]):
                self.fenElementDict['fenEP'] = self.fenElements[3]
            #else:
                #self.fenEP = 'unkonwn'

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
            # critical information
            #self.fenToPlay = 'unknown'
            # critical information
            #self.fenCastling = 'unknown'
            # critical information
            #self.fenEP = 'unknown'
            # non-critical reset to 0
            self.fenElementDict['fenHalfMoveClock'] = '0'
            # non-critical reset to 1
            self.fenElementDict['fenMoveCounter'] = '1'

            self.message = WarningMsg(header = 'Fen Error',
                body = 'incomplete fen string',
                instruction = 'please check fen has all the required elements')
            self.errorLog.append('fenError')
            self.message

        self.testBoard()
        #self.fenErrorFlagCheck()
        #self.fenIncorrectFlagCheck()

        def __repr__(self):
         return self.fen

    def testBoard(self):
    # this is a series of tests on the board to see if it valid

    # test that there are two kings on the fenBoard
    # one White and one Black
        self.whiteKing = self.fenElementDict['fenBoard'].count('K')
        self.blackKing = self.fenElementDict['fenBoard'].count('k')

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
                            self.message = WarningMsg(header = 'EP square' + fenEP,
                                body = 'The EP square is not valid in a "white to play" position')
                            self.errorLog.append('fenEPSquareInvalid')
                            self.message
                            return False

                    if self.fenElementDict.get('fenToPlay') == 'b':
                        if fenEP in self.validEPbtp:
                            return True
                        else:
                            self.message = WarningMsg(header = 'EP square' + fenEP,
                                body = 'The EP square is not valid in a "black to play" position')
                            self.errorLog.append('fenEPSquareInvalid')
                            self.message
                            return False
                else:
                    self.message = WarningMsg(header = 'EP '+ fenEP,
                        body = 'The EP Element is not a valid square')
                    self.errorLog.append('fenEPSquareInvalid')
                    self.message
                    return False

                if self.fenElementDict.get('fenToPlay' ,'unknown') == 'unknown':
                    self.message = WarningMsg(header = 'EP square ' + fenEP,
                        body = 'It is not known who it is to play',
                        instruction = 'It is not possible to check the validity of the EP square')
                    self.errorLog.append('fenEPSquareUnclear')
                    self.message
                    return False

        else:
            self.message = WarningMsg(header = '"EP" element of fen',
                body = 'This element is too long')
            self.errorLog.append('fenEPLength')
            self.message
            return False

    #def fenIncorrectFlagCheck(self):
        # check that fenBoard, fenHalfMoveClock, fenMoveCounter
        # have not been set to 'unknown'
    #    self.OKflag = True
    #    if self.fenElementDict['fenBoard' , 'unknown'] == 'unknown':
    #        self.errorLog.append('incorrectBoardFlag')
    #        self.message = WarningMsg(header = 'Error ' + fenEP,
    #            body = 'The fenBoard element has been set to "unknown"',
    #            instruction = 'This should never happen as this looses too much information')
    #        self.OKflag = False
    #    if not self.fenElementDict['fenHalfMoveClock'].isdigit():
    #        self.errorLog.append('incorrectHalfMoveFlag')
    #        self.message = WarningMsg(header = 'Error' + fenEP,
    #            body = 'The fenHalfMoveClock clock element has been set to "unknown"',
    #            instruction = 'If incorrect in original fen the figure should be reset to 0')
    #        self.OKflag = False
    #    if not self.fenElementDict['fenMoveCounter'].isdigit():
    #        self.errorLog.append('incorrectMoveFlag')
    #        self.message = WarningMsg(header = 'Error ' + fenEP,
    #            body = 'The fenMove Counter has been set to "unknown"',
    #            instruction = 'It incorrect in original fen the figure should be reset to 1')
    #        self.OKflag = False
    #    return self.OKflag

    #def fenErrorFlagCheck(self):
        #self.unknownCount = 0
        # check whether fenError flag is correct
        # if none of the elements are flagged as 'unknown'
        # then the flag is incorrect
        #self.fenIncorrectFlagCheck()

        #if 'fenError' in self.errorLog:
            # fenBoard is not checked as this should never
            # be set to 'unknown'
            #if self.fenToPlay == 'unknown':
                #self.unknownCount += 1
            #if self.fenCastling == 'unknown':
                #self.unknownCount += 1
            #if self.fenEP == 'unknown':
                #self.unknownCount += 1
            #if self.unknownCount == 0:
                #self.errorLog.remove('fenError')
            # fenHalfMoveClock and fenMoveCounter should always be a digit

# initial test
# test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq e3 1 2')
# print(test.fenElementDict.get('fenEP', 'unknown'))
















#
