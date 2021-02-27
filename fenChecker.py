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

        print('\n','*' * asterixNo,
                '\n     ',header,'\n'
                '\n     ',body,'\n')
        if instruction:
            print('\n     ',instruction,'\n')
        print('*' * asterixNo,'\n')

class Fen():

    def __init__(self, fen = ''):

        # these variables to help check elements of the fen
        # A) castling
        self.validBoardCharacters = '12345678/kqrnbpKQRBNP'
        self.validCastling =['-','q','k','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kk','Kkq','KQ','KQq','KQk',
                   'KQkq'] # copy changes to inputCastling()
        # B) EP square
        self.validEPwtp = ['-','a6','b6','c6','d6','e6','f6','g6','h6']
                # copy changes to inputEP()
        self.validEPbtp = ['-','a3','b3','c3','d3','e3','f3','g3','h3']
                # copy changes to inputEP()
        # C) board squares
        self.validSquares = ('a8','b8','c8','d8','e8','f8','g8','h8',
                            'a7','b7','c7','d7','e7','f7','g7','h7',
                            'a6','b6','c6','d6','e6','f6','g6','h6',
                            'a5','b5','c5','d5','e5','f5','g5','h5',
                            'a4','b4','c4','d4','e4','f4','g4','h4',
                            'a3','b3','c3','d3','e3','f3','g3','h3',
                            'a2','b2','c2','d2','e2','f2','g2','h2',
                            'a1','b1','c1','d1','e1','f1','g1','h1')
        # D) other
        self.errors = [] # used in the  method

        # processing of the fen starts here
        fen = str(fen) # forcing fen argument to a string
        self.fen = fen
        self.fenElements = fen.split(' ')
        self.elementCount = len(self.fenElements)
        print(self.elementCount)
        self.board = self.checkBoard(board = self.fenElements[0])

        if self.elementCount > 1: # toPlay element
            self.toPlay = self.checkToPlay(self.fenElements[1])
        else:
            self.toPlay = self.checkToPlay(toPlay = '?')

        if self.elementCount > 2: # castling element
            self.castling = self.checkCastling(board = self.board, castling = self.toPlay)
        else:
            self.castling = self.checkCastling(board = self.board, castling = "?")

        if self.elementCount > 3: # ep element
            self.ep = self.checkEP(toPlay = self.toPlay)
        else:
            self.ep = self.inputEP(toPlay = self.toPlay)

        if self.elementCount > 4:
            if self.fenElements[4].isdigit():
                self.halfMove = self.fenElements[4]
            else:
                # reset value
                self.halfMove = '0'
        else:
            # set to '0'
            self.halfMove = '0'

        if self.elementCount > 5:
            if self.fenElements[5].isdigit():
                self.move = self.fenElements[5]
            else:
                # reset value
                self.move = '1'
        else:
            #set to '1'
            self.move = '1'

    def __repr__(self):
        return self.fenReconstruct()

    # This section is for routines which check fenElements


    def checkBoard(self, board):
        # this is a series of tests on the board to see if it valid
        newBoard = ''
        self.errors.append('first time check')
        # test if fenBoard element contains only valid characters

        while not self.errors == []:
            # if the number of squares in the board is not 64 then some of the
            # subsequent methods will not work
            boardString = self.boardToString(board, checkBoard = True)
                # the boardToString method returns a string of 64 characters
                # but also appends errors to self.errors if the original board
                # was too short or too long'
                # The appending of self.error only occurs if the boardToString
                # method is called from here: hence ' = True'

            for char in board:
                if not char in self.validBoardCharacters:
                    error = ' There are invalid characters in the board string'
                    message = WarningMsg(header = 'Board Error',
                    body = error )
                    message
                    self.errors.append(error)

            # test that there are two kings on the board
            # (one White and one Black)
            whiteKings = board.count('K')
            blackKings = board.count('k')

            if whiteKings == 0:
                error = 'There is no White King on the board'
                message = WarningMsg(header = 'Illegal Position',
                    body = error)
                message
                self.errors.append(error)

            if whiteKings > 1:
                error = 'There are too many White Kings on the board'
                message = WarningMsg(header = 'Illegal Position',
                    body = error)
                message
                self.errors.append(error)

            if blackKings == 0:
                error ='There is no Black King on the board'
                message = WarningMsg(header = 'Illegal Position',
                    body = error)
                message
                self.errors.append(error)

            if blackKings > 1:
                error = 'There are too many Black Kings on the board'
                message = WarningMsg(header = 'Illegal Position',
                    body = error)
                message
                self.errors.append(error)

            if self.errors:
                self.displayBoardString(self.boardToString(board, checkBoard = True))
                print('\n')
                board= self.inputBoard(reasons = self.errors, board= board)

            self.errors = []

        return board

    def checkToPlay(self, toPlay):

        if toPlay == 'w' or toPlay == 'b':
            newToPlay = toPlay
        else:
            message = WarningMsg(header = 'Error in To Play element of fen',
                    body = str(toPlay)+' input is not valid',
                    instruction = 'should be either "w" or "b". Please re-input.')
            message
            newToPlay = self.inputToPlay()

        return newToPlay

    def checkCastling(self, castling, board):

        if not castling in self.validCastling:
            message = WarningMsg(header = 'Castling: '+str(castling),
                    body = 'The Castling Element is not in a valid form',
                    instruction = 'format "-" or up to 4 letters in order KQkq')
            message
            castling = self.inputCastling()

        boardString = self.boardToString(board)
        e1 = self.interrogateBoard(boardString = boardString, targetSquare = 'e1')
        h1 = self.interrogateBoard(boardString = boardString, targetSquare = 'h1')
        a1 = self.interrogateBoard(boardString = boardString, targetSquare = 'a1')
        e8 = self.interrogateBoard(boardString = boardString, targetSquare = 'e8')
        h8 = self.interrogateBoard(boardString = boardString, targetSquare = 'h8')
        a8 = self.interrogateBoard(boardString = boardString, targetSquare = 'a8')

        if castling == '-':
            newCastling = '-'
        else:
            newCastling = ''
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

    def checkEP(self, ep):

        if not ep == '-':
            if self.toPlay == 'w':
                if ep in self.validEPwtp:
                    newEP = ep
                else:
                    message = WarningMsg(header = 'EP square: ' + str(ep),
                            body = 'The EP square is not valid in a "white to play" position')
                    message
                    newEP = self.epInput(toPlay  = 'w')
            elif self.toPlay == 'b':
                if ep in self.validEPbtp:
                    newEP = ep
                else:
                    message = WarningMsg(header = 'EP square' + str(ep),
                            body = 'The EP square is not valid in a "black to play" position')
                    message
                    newEP = self.epInput(toPlay = 'b')
        else:
            newEP = ep

        return newEP

    # this section is for input routines which return a corrected value
    # these are static methods to allow mock input testing in pytest

    @staticmethod
    def inputBoard(board, reasons = []):

        print('\n the board element of the current string is: \n',
                    board)

        if reasons:
            print('\n the current board is incorrect because: \n',
                    reasons)

        newBoard = input('\n please input a new string which represents the position\n')

        return newBoard

    @staticmethod
    def inputToPlay():

        newToPlay = '?'
        print('\n Is it white or black is to play in this position?')
        while newToPlay not in 'wb':
            newToPlay = input('\n please input "w" or "b" \n')
            if newToPlay not in 'wb':
                print('\n*** input incorrect ***\n')
        return newToPlay

    @staticmethod
    def inputCastling():

        validCastling =['-','q','k','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kk','Kkq','KQ','KQq','KQk',
                   'KQkq']
        castling = '?'
        while not castling in validCastling:
            print('valid castling strings must be one of the following:')
            print(validCastling)
            castling = input('please input one of these\n')
            if not castling in validCastling:
                print('\n*** input incorrect ***\n')
        return castling

    @staticmethod
    def inputEP(toPlay):

        validEPwtp = ['-','a6','b6','c6','d6','e6','f6','g6','h6']
        validEPbtp = ['-','a3','b3','c3','d3','e3','f3','g3','h3']
        ep = '?'

        if toPlay == 'w':
            validSquares = validEPwtp
        else:
            validSquares = validEPbtp

        while not ep in validSquares :
            print('\nvalid inputs are:\n')
            print(validSquares)
            ep = input('\n please input "-" if no, or a valid ep square\n')
            if not ep in validSquares:
                print('\n*** input incorrect ***\n')

        return ep

    # This section is for simple display options

    def displayBoardString(self, boardString = ''):

        printable = ''
        for i in range(64):
            if i % 8 == 0:
                printable += '\n   '+boardString[i]
            else:
                printable += '   '+boardString[i]

        print(printable)

    def displayToPlay(self, toPlay = ''):
        if toPlay == '':
            self.toPlay
        if toPlay == 'w':
            print('      white to play\n')
        elif toPlay == 'b':
            print('      black to play\n')
        else:
            print('\n')

# this section is for conversions from the board representation in the
# fen to other internal representations

    def boardToString(self, board = '', checkBoard = False):
        # convert board to string
        # if the number of squares in the board is not 64 then some of the
        boardString = ''

        if board == '':
            if checkBoard: # if called by checkBoard
                self.errors.append('Empty Board')
                board = '8/8/8/8/8/8/8/8' #set to empty board
            else:
                # self.board no set if checkBoard running
                board = self.board

        #convert board to string
        for char in board:
            if char == '/':
                pass
            elif char in self.validBoardCharacters:
                if char.isdigit():
                    boardString += '.' * int(char)
                else:
                    boardString += char
            else:
                boardString += '?' # identies invalid character
        # ensure boardString is exactly 64 digits long

        if len(boardString) > 64:
            if checkBoard: # if called from checkBoard
                self.errors.append('board has too many squares')
            boardString = boardString[0:64]
        if len(boardString) < 64:
            if checkBoard: # if called from checkBoard
                self.errors.append('board has too few squares')
            paddingLength = 64 - len(boardString)
            boardString += '.' * paddingLength # add blank squares to end

        return boardString

    def boardToArray(self, board = ''):
        if board == '':
            board = self.board
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
            boardString = self.board
        return boardString[self.squareToFenPosition(targetSquare)]

    def fenReconstruct(self):
        # this will recompile the elements into a valid fen
        a = self.board+' '
        b = self.toPlay+' '
        c = self.castling+' '
        d = self.ep+' '
        e = self.halfMove+' '
        f = self.move
        return a + b + c + d + e + f


# initial test
