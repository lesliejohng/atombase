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

    def __init__(self, fen = '?'):

        # these variables to help check elements of the fen
        # A) castling
        self.recognisedCastling = ['q','k','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kk','Kkq','KQ','KQq','KQk','KQkq']
            # used to identify a castling element in a fen string
        self.validCastling = ['-','q','k','kq','Q','Qq','Qk','Qkq','K',
                   'Kq','Kk','Kkq','KQ','KQq','KQk','KQkq']
            # used to confirm a valid castling element
            # DOES NOT take into account the limitations imposed
            # by the actual position
        # B) EP square
        self.recognisedEP =['a6','b6','c6','d6','e6','f6','g6','h6',
                            'a3','b3','c3','d3','e3','f3','g3','h3']
            # used to identify an ep element in a fen string
        self.validEPwtp = ['-','a6','b6','c6','d6','e6','f6','g6','h6']
            # valid ep elements if white to play
            # DOES NOT take into account the limitations imposed
            # by the actual position
        self.validEPbtp = ['-','a3','b3','c3','d3','e3','f3','g3','h3']
            # valid ep elements if black to play
            # DOES NOT take into account the limitations imposed
            # by the actual position
        self.validEP = self.validEPwtp + self.validEPbtp
            # valid ep elements ignoring who is to play
            # DOES NOT take into account the limitations imposed
            # by the actual position
        # C) board
        self.validBoardCharacters = '12345678/kqrnbpKQRBNP'
            # valid characters for a board element of a fes string
        self.validSquares = ('a8','b8','c8','d8','e8','f8','g8','h8',
                            'a7','b7','c7','d7','e7','f7','g7','h7',
                            'a6','b6','c6','d6','e6','f6','g6','h6',
                            'a5','b5','c5','d5','e5','f5','g5','h5',
                            'a4','b4','c4','d4','e4','f4','g4','h4',
                            'a3','b3','c3','d3','e3','f3','g3','h3',
                            'a2','b2','c2','d2','e2','f2','g2','h2',
                            'a1','b1','c1','d1','e1','f1','g1','h1')
            # valid squares
        # D) other
        self.errors = [] # used in the checkBoard method

        # processing of the fen starts here
        fen = str(fen) # forcing fen argument to a string
        fen = fen.strip() # stripping leading/trailing white space

        # splitting fen into sub-strings
        self.fen = fen
        self.fenElements = fen.split(' ')

        # processing the sub-strings

        # In handling a string input I have made the following assumptions
        #       1) the first sub-string is always the board
        #       2) the last sub-string is always the move counter IF A DIGIT and fen
        #          has more at least 2 elements
        #       3) the penultimate sub-string is always the half move clock IF A DIGIT
        #          AND the last sub-string is ALSO A DIGIT and the fen has as least
        #          3 elements
        #       4) if a toPlay, castling or ep element is recognised


        self.elementCount = len(self.fenElements)

        # Here I am identifying obvious elements
        self.toPlay = '?'
        self.castling = '?'
        self.ep = '?'
        self.halfMove = '0'
        self.move = '1'

        for element in self.fenElements:
            # does element look like a ToPlay element?
            if len(element) == 1 and element in 'wb':
                self.toPlay = self.checkContradiction(existing = self.toPlay,
                                                            new = element)
            # does element look like a castling element?
            elif element in self.recognisedCastling:
                self.castling = self.checkContradiction(existing = self.castling,
                                                    new = element)
            # does element look like a ep element?
            elif element in self.recognisedEP:
                self.ep = self.checkContradiction(existing = self.ep,
                                                new = element)

        countBlank = self.fenElements.count('-')

        if countBlank > 1: # implies no castling rights and no ep square
            # if castling and ep not set make these '-'
            if self.castling == '?':
                self.castling = '-'
            if self.ep == '?':
                self.ep = '-'
        elif countBlank == 1: # problem here is which to apply the element
            if self.castling != '?' and self.ep != '?':
                pass  # any '-' will be ignored as castling and ep set
            elif self.castling != '?':
                # '-' must relate to ep square
                self.ep = '-'
            elif self.ep != '?':
                # '-' must relate to castling right
                self.castling = '-'
            else: # castling and ep element not set
                # it is not clear whether a single '-' relates to
                # castling or ep, replace '-' with '?', forcing input
                if self.castling == '?' and self.ep == '?':
                    # force input of castling and ep
                    self.fenElements = ['?' if i=='-' else i for i in self.fenElements]

        self.board = self.checkBoard(board = self.fenElements[0])

        if len(self.toPlay) == 1 and self.toPlay in 'wb':
            pass # no change required
        elif self.toPlay == '?' or self.toPlay == '??':
            self.toPlay = self.checkToPlay(toPlay = '?')
        else:
            self.toPlay = self.checkToPlay(toPlay = self.toPlay)

        if self.castling in self.validCastling:
            self.castling = self.checkCastling(castling = self.castling, board = self.board)
        elif self.castling == '?' or self.castling == '??':
            self.castling = self.checkCastling(castling = '?', board = self.board)
        else:
            self.castling = self.checkCastling(castling = self.castling, board = self.board)

        #print(self.ep)
        if self.ep in self.validEP:
            #print('__init__: valid ep')
            self.ep = self.checkEP(ep = self.ep, toPlay = self.toPlay, board = self.board)
            #print('post ep type: '+ str(type(self.ep)))
            #print('post checkEP: ' + self.ep)
        elif self.ep == '?' or self.ep == '??':
            #print('__init__: ep is ? or ??')
            self.ep = self.checkEP(ep = '?', toPlay = self.toPlay, board = self.board)
            #print('post ep type: '+ str(type(self.ep)))
            #print('post checkEP: ' + self.ep)
        else:
            #print('__init__: ep other invalid')
            self.ep = self.checkEP(ep = self.ep, toPlay = self.toPlay, board = self.board)
            #print('post ep type: '+ str(type(self.ep)))
            #print('post checkEP: ' + self.ep)

        # if penultimate item on list is a digit
        # take this as the halfMove
        if self.elementCount > 2: # must have board element plus at least 2 elements
            if self.fenElements[-2].isdigit() and self.fenElements[-1].isdigit():
            # the penultimate sub-string is not accepted is the last sub-string
            # is not also a digit
                self.halfMove = self.fenElements[-2]
            else:
                # reset value to 0
                self.halfMove = '0'
        else:
            # set to '0'
            self.halfMove = '0'

        # if last item on list is a digit
        # take this as the move
        if self.elementCount > 1: # must have board + at least 1 other sub-string
            if self.fenElements[-1].isdigit(): # floats rejected as invalid
                self.move = self.fenElements[-1]
            else:
                # reset value to 1
                self.move = '1'
        else:
            #set to '1'
            self.move = '1'

    def __repr__(self):
        return self.fenReconstruct()

    # This section is for routines which check fenElements

    def checkContradiction(self, existing, new):
        # called by __init__
        # compares two elements
        # if not cotradictory returns the new elements
        # if contradictory returns '??'

        if existing == '?': #value unset
            return new
        elif existing == '??':
            # contradictory elements in fen
            return existing # leave '??' caution in place
        else: # check for contradictions
            if  existing == new:
                # make no change to existing value
                return new
            else: #contradictory elements in fen
                return '??'
        print('Warning! checkContradiction. This should never print!')

    def checkBoard(self, board):
        # called by __init__
        # this is a series of tests on the board to see if it valid
        # responsible for checking of board
        # returns a valid and checked board
        newBoard = ''
        # to force while loop to run
        self.errors.append('first time flag')

        while not self.errors == []:

            # to remove flag
            if 'first time flag' in self.errors:
                self.errors.pop(self.errors.index('first time flag'))

            # if the number of squares in the board is not 64 then some of
            # the subsequent methods will not work
            boardString = self.boardToString(board = board, checkBoard = True)
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
                self.displayBoardString(self.boardToString(board = board, checkBoard = True))
                print('\n')
                board= self.inputBoard(reasons = self.errors, board= board)

            self.errors = []

        return board

    def checkToPlay(self, toPlay):
        # called by __init__
        # calls inputToPlay, which is responsible for returning
            # a valid toPlay element
        # returns a valid ep
        if toPlay == 'w' or toPlay == 'b':
            return toPlay
        else:
            message = WarningMsg(header = 'Error in To Play element of fen',
                    body = str(toPlay)+' input is not valid',
                    instruction = 'should be either "w" or "b". Please re-input.')
            message
            return self.inputToPlay()

    def checkCastling(self, castling, board):
        # called by __init__
        # calls inputCastling, which is responsible for returning a valid
            # castling element
        # processes to recieved value of castling by comparing it to the
            # board automatically changing castling elements where these
            # are clearly incorrect
        # returns a valid and checked castling element
        if not castling in self.validCastling:
            message = WarningMsg(header = 'Castling: '+str(castling),
                    body = 'The Castling Element is not in a valid form',
                    instruction = 'format "-" or up to 4 letters in order KQkq')
            message
            castling = self.inputCastling()

        boardString = self.boardToString(board = board)
        checkedSquares = self.interrogateBoard(boardString = boardString,
            targetSquares = ['e1','h1','a1','e8','h8','a8'])
        e1 = checkedSquares[0]
        h1 = checkedSquares[1]
        a1 = checkedSquares[2]
        e8 = checkedSquares[3]
        h8 = checkedSquares[4]
        a8 = checkedSquares[5]

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
            if newCastling != castling:
                message = WarningMsg(header = 'provided castling: ' + str(castling),
                        body = 'was inconsistant with rook and king positions',
                        instruction = 'was changed to: '+ str(newCastling))
                message

        if newCastling == '':
            newCastling = '-'

        return newCastling

    def checkEP(self, ep, toPlay, board):
        #print('checkEP in: '+ ep)
        providedEP = ep
        if ep == '-':
            newEP = ep #assumed correct
        elif ep in self.validEP:
            if toPlay == 'w':
                if ep in self.validEPwtp:
                    newEP = ep
                else:
                    message = WarningMsg(header = 'EP square: ' + str(ep),
                            body = 'The EP square is not valid in a "white to play" position')
                    message
                    newEP = self.inputEP(toPlay  = 'w')
                    providedEP = newEP
                    #print('checkEP: invalid wtp ')
                    #print(newEP)
                    #print(type(newEP))
            elif toPlay == 'b':
                if ep in self.validEPbtp:
                    newEP = ep
                else:
                    message = WarningMsg(header = 'EP square' + str(ep),
                            body = 'The EP square is not valid in a "black to play" position')
                    message
                    newEP = self.inputEP(toPlay = 'b')
                    providedEP = newEP
                    #print('checkEP: invalid btp ')
                    #print(newEP)
                    #print(type(newEP))
        else:
            newEP = self.inputEP(toPlay = toPlay)
            providedEP = newEP
            #print('checkEP: invalid ep'+ep)
            #print(newEP)
            #print(type(newEP))

        if newEP != '-': # if not set no further checks required
            boardString = self.boardToString(board = board)
            # find rank and file of ep
            file = newEP[0]
            #print(type(file))
            rank = newEP[1]
            #print(type(rank))
            if newEP == 'a6':
                checkedSquares = self.interrogateBoard(boardString = boardString,
                    targetSquares = ['a7','a5','b5'])
                if checkedSquares != ['.','p','P']:
                    newEP = '-'
            elif newEP == 'a3':
                checkedSquares = self.interrogateBoard(boardString = boardString,
                    targetSquares = ['a2','a4','b4'])
                #print(checkedSquares)
                if checkedSquares != ['.','P','p']:
                    newEP = '-'
            elif newEP == 'h6':
                checkedSquares = self.interrogateBoard(boardString = boardString,
                    targetSquares = ['h7','h5','g5'])
                if checkedSquares != ['.','p','P']:
                    newEP = '-'
            elif newEP == 'h3':
                checkedSquares = self.interrogateBoard(boardString = boardString,
                    targetSquares = ['h2','h4','g4'])
                if checkedSquares != ['.','P','p']:
                    newEP = '-'
            else:
                if toPlay == 'w':
                    movedFromRank = '7'
                    movedToRank = '5'
                    attackerRank = '5'
                    ownPawn = 'p'
                    enemyPawn = 'P'
                else:
                    movedFromRank = '2'
                    movedToRank = '4'
                    attackerRank ='4'
                    ownPawn = 'P'
                    enemyPawn = 'p'
                files = ['a','b','c','d','e','f','g','h']
                currentFileNumber = files.index(file)
                leftAttackFile = str(files[currentFileNumber-1])
                rightAttackFile = str(files[currentFileNumber+1])
                checkedSquares = self.interrogateBoard(boardString = boardString,
                                targetSquares = [file+movedFromRank,
                                        file+movedToRank,
                                        leftAttackFile+attackerRank,
                                        rightAttackFile+attackerRank])
                print(checkedSquares)
                if checkedSquares == ['.',ownPawn,enemyPawn,enemyPawn] or checkedSquares == ['.',ownPawn,enemyPawn,'.'] or checkedSquares == ['.',ownPawn,'.',enemyPawn] :
                    pass
                else:
                    newEP = '-'

            if providedEP != newEP:
                message = WarningMsg(header = 'provided ep: ' + str(providedEP),
                    body = 'was inconsistant with pawn positions',
                    instruction = 'was changed to "-"')
                message

        #print('checkEP return')
        #print(type(newEP))
        return newEP

    # this section is for input routines which return a corrected value
    # these are static methods to allow mock input testing in pytest

    def inputBoard(self, board, reasons = []):
        # called by checkBoard
        # checkBoard is responsible for verifying position
        # returns an unchecked board in fen format
        print('\n the board element of the current string is: \n',
                    board)

        if reasons:
            print('\n the current board is incorrect because: \n',
                    reasons)

        newBoard = input('\n please input a new string which represents the position\n')

        return newBoard

    def inputToPlay(self):
        # called by checkToPlay
        # returns a checked toPlay value
        newToPlay = '?'
        print('\n Is it white or black is to play in this position?')
        while newToPlay not in 'wb':
            newToPlay = input('\n please input "w" or "b" \n')
            if newToPlay not in 'wb':
                print('\n*** input incorrect ***\n')
        return newToPlay

    def inputCastling(self):
        # called by checkCastling
        # responsible to check return value against self.validCastling
        # returns a generally valid castling value
        castling = '?'
        while not castling in self.validCastling:
            print('valid castling strings must be one of the following:')
            print(self.validCastling)
            castling = input('please input one of these\n')
            if not castling in self.validCastling:
                print('\n*** input incorrect ***\n')
        return castling

    def inputEP(self, toPlay):
        # called by checkEP
        # responsible to check return against self.validEPbtp or
            # selfValidEPwtp
        # return a valid ep square
        ep = '?'

        if toPlay == 'w':
            validSquares = self.validEPwtp
        else:
            validSquares = self.validEPbtp

        while not ep in validSquares :
            print('\nvalid inputs are:\n')
            print(validSquares)
            ep = input('\n please input "-" if no ep square, or a valid ep square\n')
            if not ep in validSquares:
                print('\n*** input incorrect ***\n')

        #print(ep)
        #print(type(ep))
        return ep

    def inputSquare(self):
        # called by square ToFenPosition
        # responsible for checking return square if in self.validSquares
        # returns a valid square name
        square = '?'
        while square not in self.validSquares:
            square = input('please input a valid square')
            return square

    # This section is for simple display options

    def displayBoardString(self, boardString = ''):

        if boardString == '':
            self.boardToArray()

        printable = ''
        for i in range(64):
            if i % 8 == 0:
                printable += '\n  '+boardString[i]
            else:
                printable += '  '+boardString[i]

        print(printable)

    def displayBoard(self, boardArray = ''):

        if boardArray == '':
            self.boardToArray()

        print('\n')
        for rank in boardArray:
            print(rank)
        print('\n')

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
            if checkBoard:
                # self.board not set
                board = '8/8/8/8/8/8/8/8' #empty board
            else:
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
            boardArray = self.boardToArray(self.board)

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

# board searching

    def squareToFenPosition(self,square):
        # called by interrogateBoard
        # calls squareInput, which has responsibility to return a valid square
        # return: integer in range 0 to 63
        if square not in self.validSquares:
            square = self.inputSquare()

        return self.validSquares.index(square)

    def interrogateBoard(self, targetSquares, boardString = '' ):
        #called by checkCastling
        # returns list of pieces on each target square
        returnList = []
        if boardString == '':
            boardString = self.boardToString(board = self.board)
        for targetSquare in targetSquares:
            returnList.append(boardString[self.squareToFenPosition(targetSquare)])
        return returnList

# fen reconstruction

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
def main():
    print('starting direct tests\n')
    test=Fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e6 0 1')
    print('should be starting position with e6 as a epsquare: ')
    print(test.board, test.toPlay, test.castling, test.ep, test.halfMove, test.move)

if __name__ == '__main__' :
    main()
