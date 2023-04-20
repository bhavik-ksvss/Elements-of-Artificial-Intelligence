# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys
import copy
import math
import numpy as np

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#

'''
# another super simple algorithm: just move piece to the least-full column
while 1:
    time.sleep(0.1)

    board = quintris.get_board()
    column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
    index = column_heights.index(max(column_heights))

    if(index < quintris.col):
        quintris.left()
    elif(index > quintris.col):
        quintris.right()
    else:
        quintris.down()
'''
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    # b = left
    # m = right
    # n = rotates
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times

        temp = copy.deepcopy(quintris)

        # returns answer as [column, number of flips, number of rotations]
        column, num_flips, num_rotations = self.best_placement(temp)

        moves = []

        curr = quintris.col
        diff = abs(curr - column)
        if curr < column:
            for _ in range(len(diff)):
                moves.append('m')
        elif curr > column:
            for _ in range(diff):
                moves.append('b')


        if num_flips == 1:
            moves.append('h')

        for _ in range(num_rotations):
            moves.append('n')


        return moves

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        #print(quintris.check_collision(quintris.get_board(), 0, quintris.get_piece()[0], 10, 10))
        while True:
            time.sleep(.1)
            moves = self.get_moves(quintris)

            for move in moves:
                if move == 'b':
                    quintris.left()
                elif move == 'm':
                    quintris.right()
                elif move == 'h':
                    quintris.hflip()
                elif move == 'n':
                    quintris.rotate()


            while quintris.row > 2:
                quintris.down()

    def best_placement(self, quintris):
        # this is just so I can set up my iterator over the columns of the board
        piece = quintris.get_piece()

        # here I'm going to store [column, number flips, number rotations]
        res = []
        best = math.inf

        # I'm subtracting the width of the piece so we dont go out of bounds
        # for every possible column
        for col in range(quintris.BOARD_WIDTH - len(piece[0][0])): # need to check if a piece's width changes when it rotates or if they're always nxn matrices
            for i in range(2):
                for j in range(4): # j represents the number of rotations
                    temp = copy.deepcopy(quintris)
                    # I'm not sure if this is the right way to do it but I made a copy because I wanted
                    # to make use of the quintris movement methods but I obviously dont want to drop the
                    # actual active piece yet

                    # move to the current column
                    while temp.col != col:
                        if temp.col < col:
                            temp.right()
                        else:
                            temp.left()

                    # flip if needed
                    if i == 1:
                        temp.hflip()
                    # rotate as much as needed
                    for _ in range(j):
                        temp.rotate()

                    # here I simulate dropping the piece with it's current setup
                    # maybe I need to change this around and pass in temp, not sure if that matters or not
                    #board = temp.get_board()
                    #piece = temp.get_piece()

                    while temp.row > 2:
                        temp.down()

                    curr = self.cost(temp)



                    if curr < best:
                        best = curr
                        res = (col, i, j)


            return res # [column number, number of flips, number of rotations]


    def bumpiness(self, floor):
        sum = 0
        for i in range(1, len(floor)):
            sum += abs(floor[i-1] - floor[i])

        return sum

    # this method gets the height of the tallest resting piece in each column
    def get_floor(self, quintris):
        board = quintris.get_board()
        piece = quintris.get_piece()
        heights = []

        # top left corner and bottom right corner of piece
        p = [(piece[1], piece[2]), (piece[1]+len(piece[0]), piece[2]+len(piece[0][0]))]

        for x in range(quintris.BOARD_WIDTH):
            for y in range(quintris.BOARD_HEIGHT):
                # ignore if current coordinate is part of the falling piece
                if y >= p[0][0] and y < p[1][0] and x >= p[0][1] and x < p[1][1]:
                    continue

                curr = board[y][x]
                if curr == 'x':
                    heights.append(y)
                    break
                elif y == len(board)-1:
                    heights.append(y+1)

        return heights


    # this is for our heuristic function, I'm trying to calculate the number of holes there are in our
    # structure but it may need to get more sophisticated
    def get_holes(self, quintris):
        board = quintris.get_board()
        piece = quintris.get_piece()

        holes=0
        partial_holes = 0

        p = [(piece[1], piece[2]), (piece[1]+len(piece[0]), piece[2]+len(piece[0][0]))]


        for x in range(quintris.BOARD_WIDTH):
            found_x = False
            for y in range(quintris.BOARD_HEIGHT):
                if y >= p[0][0] and y < p[1][0] and x >= p[0][1] and x < p[1][1]:
                    continue

                if board[y][x] == 'x' and not found_x:
                    found_x = True
                elif board[y][x] == ' ' and found_x:

                    try:
                        left = board[y][x-1]
                    except:
                        left = 'x'

                    try:
                        right = board[y][x+1]
                    except:
                        right = 'x'


                    if left == 'x' and right == 'x':
                        holes +=1
                    else:
                        partial_holes += 1

        return holes, partial_holes


    def cost(self, quintris):
        holes, partials = self.get_holes(quintris)[0], self.get_holes(quintris)[1]
        bumpiness = self.bumpiness(self.get_floor(quintris))

        weights = [1, 1, 1]
        attributes = [holes, partials, bumpiness]

        return holes*weights[0] + partials*weights[1] + bumpiness*weights[2]




###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)
