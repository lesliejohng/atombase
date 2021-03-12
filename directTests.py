from fenChecker import Fen, WarningMsg

while True:
    print("""
Direct Test suit

Please select one on the following options

a) test display of board
z) to finish tests

""")
    selection = input('please select option\n')

    if selection == 'a':
        print('pre-set test\n')
        test = Fen('rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')
        # arguments given
        w = test.boardToString(board ='rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
        print('The simplest board representation looks like this ...\n')
        test.displayBoardString(w)
        print('\n')
        ait = input('press any key to continue')
        print('This adds colour...\n')
        x = test.boardToArray(board ='rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R')
        test.displayBoard(x)
        wait = input('press any key to continue')
        print('This adds rank and file markers...\n')
        y = test.augmentBoard(x)
        test.displayBoard(y)
        wait = input('press any key to continue')
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
        wait = input('press any key to continue')
        test.displayBoard()
        wait = input('press any key to continue')
        test.displayBoard()
        wait = input('press any key to continue')

    elif selection == 'z':
        break
