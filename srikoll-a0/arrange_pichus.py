#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Bhavik Kollipara  srikoll@iu.edu]
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' and is_validrc(house_map,r,c)==True and is_validdiag(house_map,r,c)]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

#this function is to check the valid positions in rows and columns to place the pichus
def is_validrc(house_map,r,c):
    track=''                    #track and track1 are strings that is used to record if we find any walls, pichu agents and as well as the current location '*'
    for col in range(0,len(house_map[0])):
        
        if(house_map[r][col]=='p' or house_map[r][col]=='X' ):
            track=track+house_map[r][col]
        if(col==c):             #adds '*' at the location we are in right now relative to the walls 'X' and pichus 'p'
            track+='*'    
    #the conditions for the pichu to be placed (col)      
    if('X*X' in track) or ('X*' in track and 'X*p' not in track) or ('*X' in track and 'p*X' not in track) or track == '*':
        track1=''
        
        for row in range(0,len(house_map)):
            if(house_map[row][c]=='p' or house_map[row][c]=='X' ):
                track1=track1+house_map[row][c]
            if(row==r):
                track1+='*'   
                
    #the conditions for the pichu to be placed (row) 
        if('X*X' in track1) or ('X*' in track1 and 'X*p' not in track1) or ('*X' in track1 and 'p*X' not in track1) or track1 == '*':
            return True                                                                                                                    
        else: 
            return False 
    else:
        return False

def is_validdiag(house_map,r,c):
    row=r
    col=c
    while row-1>0 and col+1< len(house_map[0]):
        if house_map[row-1][col+1]=='X':
            flag=True
            break
        elif house_map[row-1][col+1]=='p':
            return False
        else:
            row=row-1
            col=col+1
    row=r
    col=c   
    while row-1>=0 and col-1>=0:
        if house_map[row-1][col-1]=='X':
            flag=True
            break
        elif house_map[row-1][col-1]=='p':
            return False
        else:
            row=row-1
            col=col-1
    row=r
    col=c   
    while row+1<len(house_map) and col+1<len(house_map[0]):
        if house_map[row+1][col+1]=='X':
            flag=True
            break
        elif house_map[row+1][col+1]=='p':
            return False
        else:
            row=row+1
            col=col+1
    row=r
    col=c   
    while row+1<len(house_map) and col-1>=0:
        if house_map[row+1][col-1]=='X':
            flag=True
            break
        elif house_map[row+1][col-1]=='p':
            return False
        else:
            row=row+1
            col=col-1
    return flag
            
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
    return (house_map,False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


