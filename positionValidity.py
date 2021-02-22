from colorama import init
init()
from colorama import Fore, Back, Style

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
        print('\n')
        self.dline()
        c = Fore.RED
        d = Style.RESET_ALL
        print("\n     "+self.header+"\n")
        print("\n     "+self.body+"\n")
        if self.instruction:
            print("\n     "+self.instruction+"\n")
        self.dline()

# approach
# create fen class
# define the representation of the class as a fen string
# build into the fen class self checks about validity of the chess
# position represented in the initial fen string
# if possible the class will correct any errors in the initial fen
# before outputting a valid string

class Fen():

    def __init__(self,
        fen ='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        testList = []):

        # Variables required for checking fen elements
            # A) castling
        self.validBoardCharacters = '12345678/kqrnbpKQRBNP'
        self.validCastling =['-','q','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kkq','Kq','Kk','Kkq','KQ','KQq','KQk',
                   'KQkq']
            # B) valid EP square
        self.validEPwtp = ['a6','b6','c6','d6','e6','f6','g6','h6']
        self.validEPbtp = ['a3','b3','c3','d3','e3','f3','g3','h3']

        # required
        self.fenElementDict = {}
        self.testList = testList

        # initial processing
        if isinstance(fen, str):
            self.fen = fen
            self.fenElements = fen.split(' ')
            self.fenElementDict['fenBoard']= self.fenElements[0]

            if len(self.fenElements) == 6:
                # the to play information is required to check the ep
                # square, so this must be set first
                self.fenElementDict['fenToPlay'] = self.identifyToPlay(self.fenElements[1])
                self.fenElementDict['fenCastling'] = self.identifyCastling(self.fenElements[2])
                self.fenElementDict['fenEP'] = self.identifyEP(self.fenElements[3])
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
                self.directPartFenInput()

        else:
            self.message = WarningMsg(header = 'Fen Error',
                    body = 'input is not a string',
                    instruction = 'please re-input')
            self.message
            self.directFullFenInput()

        self.testBoard()

    def __repr__(self):
        return self.fen

    # This section is for routines which identify fenElements


    def identifyToPlay(self, fenToPlay):
        # ToPlay consists of a single 'w' or 'b' character
        if fenToPlay == 'w' or fenToPlay == 'b':
            return fenToPlay
        else:
            self.message = WarningMsg(header = 'Error in To Play element of fen',
                    body = str(fenToPlay)+' input is not valid',
                    instruction = 'should be either "w" or "b". Please re-input.')
            self.message
            return self.toPlayInput(newToPlay = fenToPlay, testList = self.testList)

    def identifyCastling(self,fenCastling):
        if not 'fenToPlay' in self.fenElementDict.keys():
            self.toPlayInput()

        if fenCastling in self.validCastling:
            return fenCastling
        else:
            self.message = WarningMsg(header = 'Castling: '+str(fenCastling),
                    body = 'The Castling Element is not in a valid form',
                    instruction = 'format "-" or up to 4 letters in order KQkq')
            self.message
            return self.castlingInput()

    def identifyEP(self,fenEP):
        if fenEP == '-':
                return fenEP
        elif self.fenElementDict.get('fenToPlay') == 'w':
            return self.identifyEPwtp(fenEP)
        elif self.fenElementDict.get('fenToPlay') == 'b':
            return self.identifyEPbtp(fenEP)
        else:
            return self.epInput()

    def identifyEPwtp(self,fenEP):
        if fenEP in self.validEPwtp:
            return fenEP
        else:
            self.message = WarningMsg(header = 'EP square: ' + str(fenEP),
                        body = 'The EP square is not valid in a "white to play" position')
            self.message
            return self.epInput()

    def identifyEPbtp(self,fenEP):
        if fenEP in self.validEPbtp:
            return fenEP
        else:
            self.message = WarningMsg(header = 'EP square' + str(fenEP),
                    body = 'The EP square is not valid in a "black to play" position')
            self.message
            return self.epInput()

    # This section is for input routines whre the routine
    # test_fenElements the respective key in the dictionary directly

    def directInputBoard(self):
        # temporary
        # set board to starting position
        self.fenElementDict['fenBoard'] = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    def directAmendBoard(self):
        # temporary
        # set board to starting position
        self.fenElementDict['fenBoard'] = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        # eventually this will display the board and allow user to
        # amend it

    def directPartFenInput(self):
        # case of incomplete fen
        # temporary
        # sets all but fenBoard as if it ws the starting position
        self.fenElementDict['fenToPlay'] = 'w'
        self.fenElementDict['fenCastling'] = 'KQkq'
        self.fenElementDict['fenEP'] = '-'
        self.fenElementDict['fenHalfMoveClock'] = '0'
        self.fenElementDict['fenMoveCounter'] = '1'

    def directFullFenInput(self):
        # temporary
        # set these values to starting position
        self.fenElementDict['fenBoard'] = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        self.fenElementDict['fenToPlay'] = 'w'
        self.fenElementDict['fenCastling'] = 'KQkq'
        self.fenElementDict['fenEP'] = '-'
        self.fenElementDict['fenHalfMoveClock'] = '0'
        self.fenElementDict['fenMoveCounter'] = '1'

    # this section is for input routines which return a corrected value

    @staticmethod
    def toPlayInput(newToPlay = '?',testList = []):
        if 'toPlay' in testList:
            return 'w'
        wb = ''
        print('\n Is it white or black is to play in this position?')
        while str(newToPlay) not in 'wb':
            wb = input('\n please input "w" or "b" \n')
            newToPlay = wb.lower()
            if str(newToPlay) not in 'wb':
                print('\n*** input incorrect ***\n')
        return newToPlay

    def castlingInput(self):
        # temporary
        # set castling to call
        return 'KQkq'

    def epInput(self):
        # temporary
        # set ep to none
        return '-'

    # This section is for deeper validity checks
    # these
    def testBoard(self):
        # this is a series of tests on the board to see if it valid

        # test if fenBoard element contains only valid characters
        for char in self.fenElementDict.get('fenBoard'):
            if not char in self.validBoardCharacters:
                self.message = WarningMsg(header = 'Board Error',
                    body = 'There are invalid characters in fenBoard')
                self.message
                self.directInputBoard()

        # test that there are two kings on the fenBoard
        # one White and one Black
        self.whiteKing = self.fenElementDict['fenBoard'].count('K')
        self.blackKing = self.fenElementDict['fenBoard'].count('k')

        if self.whiteKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no White King on the board')
            self.message
            self.directAmendBoard()

        if self.whiteKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many White Kings on the Board')
            self.message
            self.directAmendBoard()

        if self.blackKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no Black King on the board')
            self.message
            self.directAmendBoard()

        if self.blackKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many Black Kings on the board')
            self.message
            self.directAmendBoard()

# This section is for simple display options

    def displayBoard(self, board):
        rankCount = 0
        print('\n')
        for rank in board:
            print(board[rankCount])
            rankCount += 1

    def displayToPlay(self, toPlay):
        if toPlay == 'w':
            print('      white to play\n')
        elif toPlay == 'b':
            print('      black to play\n')
        else:
            print('\n')

# this section is for other items

    def boardToArray(self, board):
        boardArray = []
        rank = '  '
        for char in board:
            if char == '/':
                rank += ('\n')
                boardArray.append(rank)
                rank = '  '
            elif char in self.validBoardCharacters:
                if char.isdigit():
                    count = int(char)
                    for x in range(count):
                        rank += '.   '
                else:
                    if char.islower():
                        rank += Fore.RED + char + '   ' + Style.RESET_ALL
                    else:
                        rank += char + '   '
            else:
                rank += '?   '
        boardArray.append(rank + '\n')
        return boardArray

    def augmentBoard(self, boardArray):
        augmentedBoard = []
        augmentedBoard.append(Fore.GREEN+'\n        a   b   c   d   e   f   g   h  \n'+Style.RESET_ALL)
        augmentedRank = Fore.GREEN+'  8   '+Style.RESET_ALL
        rankCount = 8
        for rank in boardArray:
            augmentedRank = augmentedRank + rank
            augmentedBoard.append(augmentedRank)
            rankCount -= 1
            augmentedRank = Fore.GREEN+'  ' + str(rankCount) + '   '+Style.RESET_ALL
        return augmentedBoard

    def fenReconstruct(self):
        # this will recompile the elements into a valid fen
        a = self.fenElementDict.get('fenBoard')+' '
        b = self.fenElementDict.get('fenToPlay')+' '
        c = self.fenElementDict.get('fenCastling')+' '
        d = self.fenElementDict.get('fenEP')+' '
        e = self.fenElementDict.get('fenHalfMoveClock')+' '
        f = self.fenElementDict.get('fenMoveCounter')
        return a + b + c + d + e + f


# initial test
#print(Fen.toPlayInput('W'))
#a = Fen()
#print('toPlay = '+ a.toPlayInput())
















#
