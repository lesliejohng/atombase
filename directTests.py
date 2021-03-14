from fenChecker import Fen, WarningMsg

while True:
    print("""
Direct Tests

Please select one on the following options

a) test display of board
b) test too many pawns
c) pawns on 1st or 8th rank
z) to finish tests

""")
    selection = input('please select option\n')

# -----------------------------------------------------------------------------
    if selection == 'a':
        print('pre-set test\n')
        test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # arguments given
        w = test.boardToString(board ='rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
        print('The simplest board representation looks like this ...\n')
        test.displayBoardString(w)
        print('\n')
        wait = input('press any key to continue\n')
        print('This adds colour...\n')
        x = test.boardToArray(board ='rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
        test.displayBoard(x)
        wait = input('press any key to continue\n')
        print('This adds rank and file markers...\n')
        y = test.augmentBoard(x)
        test.displayBoard(y)
        wait = input('press any key to continue\n')
        print('\n')
        print("""

self input test

Please input the board element of a fen
and check the display.

    """)
        print("""
you may wish to copy this:-
rnbqkbnr/pp1ppppp/8/8/2p5/4P3/PPPP1PPP/RNBQKBNR

or you can type your own!
""")
        test.inputBoard(board = "8/8/8/8/8/8/8/8",
            reasons = ['please input test position'])
        test.displayBoardString()
        print('\n')
        wait = input('press any key to continue\n')
        test.displayBoard()
        wait = input('press any key to continue\n')
        test.displayBoard()
        wait = input('press any key to continue\n')

# -----------------------------------------------------------------------------
    elif selection == 'b':
        print("""

for these tests the correct board element of the fen is:-
rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R

copy the above to save typing!

\n""")
        print('too many white pawns\n')
        test = Fen('rnbqkbnr/pppp1ppp/8/4P3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        wait = input('press any key to continue\n')

        print('too many black pawns\n')
        test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4p3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        wait = input('press any key to continue\n')


# -----------------------------------------------------------------------------
    elif selection == 'c':
        print("""

for these tests the correct board element of the fen is:-
rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R

copy the above to save typing!

\n""")
        print('white pawns on 1st rank\n')
        test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPP2PPP/RNPQKB1R b KQkq - 1 2')
        wait = input('press any key to continue\n')

        print('white pawns on 8th rank\n')
        test = Fen('rnbqkPnr/pppp1ppp/8/4p3/4P3/5N2/PPP2PPP/RNBQKB1R b KQkq - 1 2')
        wait = input('press any key to continue\n')

        print('black pawns on 1st rank\n')
        test = Fen('rnbqkbnr/ppp2ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKp1R b KQkq - 1 2')
        wait = input('press any key to continue\n')

        print('black pawns on 8th rank\n')
        test = Fen('rnbqkpnr/ppp2ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        wait = input('press any key to continue\n')



    elif selection == 'z':
        break

    else:
        print('incorrect selection, please try again')
