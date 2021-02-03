# approach
# create fen class
# define the representation of the class as a fen string
# build into the fen class self checks about validity of the chess
# position represented in the initial fen string
# if possible the class will correct any errors in the initial fen
# before outputting a valid string

def dline():
    print('*' * 60)

class Fen():
  def __init__(self, fen):
      self.fen = fen
      self.fenElements = fen.split(' ')
      self.fenBoard = self.fenElements[0]
      if len(self.fenElements) == 6:
         self.fenToPlay = self.fenElements[1]
         self.fenCastling = self.fenElements[2]
         self.fenEP = self.fenElements[3]
         self.fenHalfMoveClock = self.fenElements[4]
         self.fenMoveCounter = self.fenElements[5]

         self.testBoard()

      else:
          dline()
          print("""

          incomplete fen string
          string does not contain all
          the expected information

          Please recheck: you will be asked
          for more information

          """)
          dline()

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
        dline()
        print("""

        There is no White King on
        the board

        """)
        dline()
    if self.whiteKing > 1:
        dline()
        print("""

        There are too many
        White kings on the board

        """
        )
        dline()
    if self.blackKing == 0:
        dline()
        print("""

        There is no Black King on
        the board

        """
        )
        dline()
    if self.blackKing > 1:
        dline()
        print("""

        There are too many
        Black kings on the board

            """
        )
        dline()







test = Fen('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')

print(test)
print(test.fenElements)
print(test.fenBoard)
print(test.fenToPlay)
print(test.fenCastling)
print(test.fenEP)
print(test.fenHalfMoveClock)
print(test.fenMoveCounter)

















#
