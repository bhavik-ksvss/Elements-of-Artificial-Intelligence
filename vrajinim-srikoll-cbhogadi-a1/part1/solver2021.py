#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    return True

# check if we've reached the goal
def is_goal(state):
    return False

def man(tile_board):
    fn=0
    for i in range(0,5):
        for j in range(0,5):
            if tile_board[i][j]%5!=0:
                fn+=abs(i-(int(tile_board[i][j]/5)))+abs(j-(tile_board[i][j]%5-1))
            else:
                fn+=abs(i-(int(tile_board[i][j]/5-1)))+abs(j-4)
    return fn

def moves(board,m):
    if 'R'in m:
        board=board[0:int(m[1])-1]+[board[int(m[1])-1][-1:]+board[int(m[1])-1][:-1]]+board[int(m[1]):]

    if 'L'in m:
        board=board[0:int(m[1])-1]+[board[int(m[1])-1][1:]+board[int(m[1])-1][:1]]+board[int(m[1]):]

    if 'D'in m:
        board=[board[0][:int(m[1])-1]+board[-1][int(m[1])-1:int(m[1])]+board[0][int(m[1]):]]+[board[1][:int(m[1])-1]+board[0][int(m[1])-1:int(m[1])]+board[1][int(m[1]):]]+[board[2][:int(m[1])-1]+board[1][int(m[1])-1:int(m[1])]+board[2][int(m[1]):]]+[board[3][:int(m[1])-1]+board[2][int(m[1])-1:int(m[1])]+board[3][int(m[1]):]]+[board[-1][:int(m[1])-1]+board[3][int(m[1])-1:int(m[1])]+board[-1][int(m[1]):]]

    if 'U'in m:
        board=[board[0][:int(m[1])-1]+board[1][int(m[1])-1:int(m[1])]+board[0][int(m[1]):]]+[board[1][:int(m[1])-1]+board[2][int(m[1])-1:int(m[1])]+board[1][int(m[1]):]]+[board[2][:int(m[1])-1]+board[3][int(m[1])-1:int(m[1])]+board[2][int(m[1]):]]+[board[3][:int(m[1])-1]+board[-1][int(m[1])-1:int(m[1])]+board[3][int(m[1]):]]+[board[-1][:int(m[1])-1]+board[0][int(m[1])-1:int(m[1])]+board[-1][int(m[1]):]]

    if 'O'in m:
        if m=='Oc':
            board=[board[1][:1]+board[0][:4]]+[board[2][:1]+board[1][1:4]+board[0][4:]]+[board[3][:1]+board[2][1:4]+board[1][4:]]+[board[4][:1]+board[3][1:4]+board[2][4:]]+[board[4][1:]+board[3][4:]]
        if m=='Occ':
            board=[board[0][1:]+board[1][4:]]+[board[0][:1]+board[1][1:4]+board[2][4:]]+[board[1][:1]+board[2][1:4]+board[3][4:]]+[board[2][:1]+board[3][1:4]+board[4][4:]]+[board[3][:1]+board[4][:4]]

    if 'I' in m:
        if m=='Ic':
            board=board[:1]+[board[1][:1]+board[2][1:2]+board[1][1:3]+board[1][4:]]+[board[2][:1]+board[3][1:2]+board[2][2:3]+board[1][3:4]+board[2][4:]]+[board[3][:1]+board[3][2:4]+board[2][3:4]+board[3][4:]]+board[4:]
        if m=='Icc':
            board=board[:1]+[board[1][:1]+board[1][2:4]+board[2][3:4]+board[1][4:]]+[board[2][:1]+board[1][1:2]+board[2][2:3]+board[3][3:4]+board[2][4:]]+[board[3][:1]+board[2][1:2]+board[3][1:3]+board[3][4:]]+board[4:]
    # move={}
    # for i in range(1,6):
    #     move['R'+str(i)]=board[i-1][-1:]+board[i-1][:-1]
    #     move['L'+str(i)]=board[i-1][1:]+board[i-1][:1]
    #     move['D'+str(i)]=board[-1][i-1:i]+board[0][i-1:i]+board[1][i-1:i]+board[2][i-1:i]+board[3][i-1:i]
    #     move['U'+str(i)]=board[1][i-1:i]+board[2][i-1:i]+board[3][i-1:i]+board[-1][i-1:i]+board[0][i-1:i]
        
    return(board)

def solver(tile_board,mov):
    min=man(tile_board)
    if min==0:
        return tile_board,mov
    move=''
    heu_set=[]
    for i in range(1,6):
        heu_set.append((man(moves(tile_board,'R'+str(i))),'R'+str(i)))
        heu_set.append((man(moves(tile_board,'L'+str(i))),'L'+str(i)))
        heu_set.append((man(moves(tile_board,'D'+str(i))),'D'+str(i)))
        heu_set.append((man(moves(tile_board,'U'+str(i))),'U'+str(i)))

        if min>man(moves(tile_board,'R'+str(i))):
            move='R'+str(i)
        if min>man(moves(tile_board,'L'+str(i))):
            move='L'+str(i)
        if min>man(moves(tile_board,'D'+str(i))):
            move='D'+str(i)
        if min>man(moves(tile_board,'U'+str(i))):
            move='U'+str(i)

    for i in ['c','cc']:
        heu_set.append((man(moves(tile_board,'O'+str(i))),'O'+str(i)))
        heu_set.append((man(moves(tile_board,'I'+str(i))),'I'+str(i)))
        if min>man(moves(tile_board,'O'+str(i))):
                move='O'+str(i)
        if min>man(moves(tile_board,'I'+str(i))):
                move='I'+str(i)

    heu_set.sort()
    for i in range(0,len(heu_set)):
        a,b=solver(moves(tile_board,heu_set[i][1]),mov=mov+' '+(heu_set[i][1]))
        if man(a)==0:
            return a,b

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    tile_board=list(list(initial_board))
    tile_board=[[tile_board[5*i+j] for j in range(0,5)]for i in range(0,5)]
    move=''
    move_set=[]
    tile_board,move=solver(tile_board,move)
    move_set=list(move.split(" "))
    move_set=move_set[1:]

    # board=[[]]
    # board=[[i*5+j for j in range(1,6)]for i in range(0,5)]
    # print(board)
    # print(tile_board)
    # print(man(tile_board),man(board))
    # print(man(moves(tile_board,'Icc')))
    # for 
    
    return move_set

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
