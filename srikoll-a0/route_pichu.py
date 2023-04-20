#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Bhavik Kollipara srikoll@u.edu]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import collections
import sys



# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

#giving the different moves names
def directions(move1,move2):
        
        path=''
        if move1[1]==move2[1]:
                if move2[0]>move1[0]:
                        path=path+'U'   
                else:
                        path=path+'D'

        if move1[0]==move2[0]:
                if move2[1]>move1[1]:
                        path=path+'R'
                else:
                        path=path+'L'
        return(path)
        



#def path(startnode, endnode, parentnode):


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        
        costpath=''
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=collections.deque([(pichu_loc,0,costpath)])
        nodes_VISITED= [[False for col in range(len(house_map[0]))] for row in range(len(house_map))]
        list1=[pichu_loc]
        dict1={}
        
        print(list1)
                
       
        
        print(fringe)

        while fringe:
                node=fringe.popleft()
                print(node)
               

                curr_move,curr_dist=node[0],node[1]
                
               
                nodes_VISITED[curr_move[0]][curr_move[1]]=True
                #parent_node.append(curr_move)
                
                
             
                for move in moves(house_map,curr_move[0],curr_move[1]):
                        
                        if nodes_VISITED[move[0]][move[1]]==False:
                                if house_map[move[0]][move[1]]=="@":
                                        dict1[move]=curr_move
                                        print(dict1)
                                        
                                        return (curr_dist+1, costpath[0:curr_dist+1])
                                        
                                else:   
                                        
                                        fringe.append((move, curr_dist + 1))
                                        dict1[move]=curr_move
                                        
                                        
                                        costpath=costpath+(directions(move,curr_move))
                                        
        return(-1," ")

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

