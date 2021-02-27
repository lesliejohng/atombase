from colorama import init
init()
from colorama import Fore, Back, Style
# I use these imports to product coloured text output

class WarningMsg():
    # I produce warnings about errors in a set way
    def __init__(self,
                    header = "Warning",
                    body = "Add your warning here",
                    instruction = "",
                    asterixNo = 60):
        # I receive two or three lines of text and can adjust the
        self.header = header
        self.body = body
        self.instruction = instruction
        self.asterixNo = asterixNo
        self.printMessage()

    def dline(self):
        # I print a line os stars on the screen
        print('*' * self.asterixNo)

    def printMessage(self):
        # I display the two/three lines of text between two
        # lines of text
        print('\n')
        self.dline()
        print("\n     "+self.header+"\n")
        print("\n     "+self.body+"\n")
        # I always print these but ...
        if self.instruction:
            print("\n     "+self.instruction+"\n")
            # ... only print this line if it is given to me
        self.dline()

class Fen():
    # I receive a fen string, check it, allow amendment bu the
    # user and return a corrected version

    def __init__(self,
        fen ='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        testList = []):
        # If I am not given a fen string I default to the Starting
        # position

        # ***********************************************************

        # I create these variables to help me check elements of
        # the fen

            # A) castling
        self.validBoardCharacters = '12345678/kqrnbpKQRBNP'
        self.validCastling =['-','q','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kkq','Kq','Kk','Kkq','KQ','KQq','KQk',
                   'KQkq']
            # B) EP square
        self.validEPwtp = ['a6','b6','c6','d6','e6','f6','g6','h6']
        self.validEPbtp = ['a3','b3','c3','d3','e3','f3','g3','h3']
            # C) squares
        self.validSquares = ('a8','b8','c8','d8','e8','f8','g8','h8',
                            'a7','b7','c7','d7','e7','f7','g7','h7',
                            'a6','b6','c6','d6','e6','f6','g6','h6',
                            'a5','b5','c5','d5','e5','f5','g5','h5',
                            'a4','b4','c4','d4','e4','f4','g4','h4',
                            'a3','b3','c3','d3','e3','f3','g3','h3',
                            'a2','b2','c2','d2','e2','f2','g2','h2',
                            'a1','b1','c1','d1','e1','f1','g1','h1')

        # **************************************************************

        # I create and use these variables later
        self.fenElementDict = {}
        # The individual elements of fen are held here under the
        # keys 'fenBoard', 'fenToMove', 'fenCastling', 'fenEP',
        # 'fenHalfMove', 'fenMove'
        self.testList = testList
        # I use a list of items to identify whether a particular
        # element is being tested by pytest. If so that element is
        # set to a known default allowing pytest to check output
        # against an expected value. The flag names I use in this
        # list are: 'board', 'toMove', 'castling', 'ep', 'halfMove'
        # and 'move'

        # *************************************************************

        # here I start to process the fen string into it's elements.
        # __init__ is directly responsible for building
        # fenElementDict
        if isinstance(fen, str):
            self.fen = fen
            self.fenElements = fen.split(' ')
            self.fenElementDict['fenBoard']= self.fenElements[0]
            # I check fenBoard is later as the process is the most
            # complex. I have chosen a dictionary to hold This
            # this information to allow a simple check on whether
            # a paticular element is missing
            if len(self.fenElements) == 6:
                # I use this check to identify incomplete fen strings
                # The processes below pass the initial values to methods
                # which
                    #   a)  identify whether the element is in the the correct
                    #       format
                    #   b)  correct the input or
                    #   c)  allow the user to change the element
                self.toPlay = self.identifyToPlay(self.fenElements[1])
                self.castling = self.identifyCastling(self.fenElements[2])
                self.fenElementDict['fenEP'] = self.identifyEP(self.fenElements[3])
                if self.fenElements[4].isdigit():
                    self.fenElementDict['fenHalfMove'] = self.fenElements[4]
                else:
                    # as this is not normally critical I reset a non digit to 0
                    # NB I keep fenHalfMoveClock and fen moveCounter as a string
                    # to allow easier reconstruction of a corrected fen
                    self.fenElementDict['fenHalfMove'] = '0'
                if self.fenElements[5].isdigit():
                    self.fenElementDict['fenMove'] = self.fenElements[5]
                else:
                    # as positions often reset the move number to 1 I reset it
                    # to 1 if the original fen element is a non digit
                    self.fenElementDict['fenMove'] = '1'
            else:
                # If some of the later elements of the fen are missing I have
                # decided to reset them completely
                # firstly I display a warning of the error
                self.message = WarningMsg(header = 'Fen Error',
                    body = 'incomplete fen string',
                    instruction = 'please check fen has all the required elements')
                self.message
                # Then I pass the processing onto a method which seeks
                # input for each of them in turn
                self.response = self.directPartFenInput()
                # I receive a collection from this method which is
                # allocated as follows
                self.toPlay = self.response[0]
                self.castling = self.response[1]
                self.fenElementDict['fenEP'] = self.response[2]
                self.fenElementDict['fenHalfMove'] = self.response[3]
                self.fenElementDict['fenMove'] = self.response[4]


        else:
            # **ICO** fen not a string
            # Here I capture the situation where the provided fen
            # is not a string and ...
            self.message = WarningMsg(header = 'Fen Error',
                    body = 'input is not a string',
                    instruction = 'please re-input')
            self.message
            # ... ask for the whole fen string to be re-input
            self.response = self.directFullFenInput()
            # I recieve from this method a collection in the following
            # order
            self.fenElementDict['fenBoard'] = self.response[0]
            self.toPlay = self.response[1]
            self.castling = self.response[2]
            self.fenElementDict['fenEP'] = self.response[3]
            self.fenElementDict['fenHalfMove'] = self.response[4]
            self.fenElementDict['fenMove'] = self.response[5]

        self.fenElementDict['fenBoard'] = self.testBoard()
        self.checkCastling(castling = self.fenElementDict.get('fenCastling'))

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

    # This section is for input routines where the routine
    # allows the element to be directly added
    # these functions receive no arguments and directly set the
    # respective test_fenElements

    def directInputBoard(self):
        # temporary
        # set board to starting position
        return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    def directAmendBoard(self, board = ''):
        # temporary
        # set board to starting position
        if board == '':
            if isinstance(self.fenElementDict.get('fenBoard'),str):
                board = self.fenElementDict.get('fenBoard')
        else:
            board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        newBoard = ''

        for char in board:
            if char in self.validBoardCharacters:
                newBoard += char
            else:
                #temp eventually user input Here
                newBoard += 'p'

        return newBoard
        # eventually this will display the board and allow user to
        # amend it

    def directPartFenInput(self):
        # case of incomplete fen
        # temporary
        # sets all but fenBoard as if it ws the starting position
        return ['w', 'KQkq', '-', '0', '1']

    def directFullFenInput(self):
        # temporary
        # set these values to starting position
        newBoard = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
            # temp will receive input of new board string from user

        return [newBoard] + self.directPartFenInput()

    # this section is for input routines which return a corrected value

    @staticmethod
    def toPlayInput(newToPlay = '?', testList = []):
        if 'toPlay' in testList:
            return 'w'
        wb = ''
        print('\n Is it white or black is to play in this position?')
        while newToPlay not in 'wb':
            wb = input('\n please input "w" or "b" \n')
            newToPlay = wb.lower()
            if newToPlay not in 'wb':
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

    def squareInput(self):
        # temporary
        # set to position of 'e8' ie 0
        return 0

    # This section is for deeper validity checks
    # these
    def testBoard(self, board = ''):
        # this is a series of tests on the board to see if it valid
        if board == '':
            board = self.fenElementDict.get('fenBoard')
        newBoard = ''
        # test if fenBoard element contains only valid characters
        for char in board:
            if not char in self.validBoardCharacters:
                self.message = WarningMsg(header = 'Board Error',
                    body = 'There are invalid characters in fenBoard')
                self.message
                newBoard = self.directAmendBoard()

        # test that there are two kings on the fenBoard
        # one White and one Black
        self.whiteKing = board.count('K')
        self.blackKing = board.count('k')

        if self.whiteKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no White King on the board')
            self.message
            newBoard = self.directAmendBoard()

        if self.whiteKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many White Kings on the Board')
            self.message
            newBoard = self.directAmendBoard()

        if self.blackKing == 0:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There is no Black King on the board')
            self.message
            newBoard = self.directAmendBoard()

        if self.blackKing > 1:
            self.message = WarningMsg(header = 'Illegal Position',
                body = 'There are too many Black Kings on the board')
            self.message
            newBoard = self.directAmendBoard()

        return newBoard

    def checkCastling(self, board = '', castling = '?'):

        if board == '':
            board = self.fenElementDict.get('fenBoard')

        newCastling = ''

        boardString = self.boardToString(board)
        e1 = self.interrogateBoard(boardString = boardString, targetSquare = 'e1')
        h1 = self.interrogateBoard(boardString = boardString, targetSquare = 'h1')
        a1 = self.interrogateBoard(boardString = boardString, targetSquare = 'a1')
        e8 = self.interrogateBoard(boardString = boardString, targetSquare = 'e8')
        h8 = self.interrogateBoard(boardString = boardString, targetSquare = 'h8')
        a8 = self.interrogateBoard(boardString = boardString, targetSquare = 'a8')

        if castling == '?':
            if e1 == 'K' and h1 == 'R':
                newCastling += 'K'
            if e1 == 'K' and a1 == 'R':
                newCastling += 'Q'
            if e8 == 'k' and h8 == 'r':
                newCastling += 'k'
            if e8 == 'k' and a8 == 'r':
                newCastling += 'q'
        elif castling == '-':
            newCastling = '-'
        else:
            for char in castling:
                if char == 'K':
                    if e1 == 'K' and h1 == 'R':
                        newCastling += 'K'
                if char == 'Q':
                    if e1 == 'K' and a1 == 'R':
                        newCastling += 'Q'
                if char == 'k':
                    if e8 == 'k' and h8 == 'r':
                        newCastling += 'k'
                if char == 'q':
                    if e8 == 'k' and a8 == 'r':
                        newCastling += 'q'

        if newCastling == '':
            newCastling = '-'
        return newCastling





# This section is for simple display options

    def displayBoard(self, board = ''):
        if board == '':
            board = self.fenElementDict.get('fenBoard')
        rankCount = 0
        print('\n')
        for rank in board:
            print(board[rankCount])
            rankCount += 1

    def displayToPlay(self, toPlay = ''):
        if toPlay == '':
            self.fenElementDict.get('fenToPlay')
        if toPlay == 'w':
            print('      white to play\n')
        elif toPlay == 'b':
            print('      black to play\n')
        else:
            print('\n')

# this section is for other items

    def boardToString(self, board = ''):
        if board == '':
            board = self.fenElementDict.get('fenBoard')
        boardString=''
        for char in board:
            if char == '/':
                pass
            elif char in self.validBoardCharacters:
                if char.isdigit():
                    count = int(char)
                    for x in range(count):
                        boardString += '.'
                else:
                    boardString += char
            else:
                boardString += '?'
        return boardString

    def boardToArray(self, board = ''):
        if board == '':
            board = self.fenElementDict.get('fenBoard')
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

    def augmentBoard(self, boardArray = []):
        if boardArray == [] :
            boardArray = self.fenElementDict.get['fenBoard']
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

    def squareToFenPosition(self,square):
        if square in self.validSquares:
            return self.validSquares.index(square)
        else:
            return self.squareInput()

    def interrogateBoard(self, targetSquare, boardString = '' ):
        if boardString == '':
            boardString = self.fenElementDict.get('fenBoard')
        return boardString[self.squareToFenPosition(targetSquare)]

    def fenReconstruct(self):
        # this will recompile the elements into a valid fen
        a = self.fenElementDict.get('fenBoard')+' '
        b = self.fenElementDict.get('fenToPlay')+' '
        c = self.fenElementDict.get('fenCastling')+' '
        d = self.fenElementDict.get('fenEP')+' '
        e = self.fenElementDict.get('fenHalfMove')+' '
        f = self.fenElementDict.get('fenMove')
        return a + b + c + d + e + f


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
c = test.checkCastling(board =board)
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
c = test.checkCastling(board =board)
print('castling nothing passed: ' + c)
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
c = test.checkCastling(board =board)
print('castling nothing passed: ' + c)
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
