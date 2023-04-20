# a0

## Question1:
To find the optimal path from the current pichu position to @(watching video lecture). It was considered that the house_map is divided in to N * M
rows and columns. The constraint added here is there are walls and the pichus can't be passed through the walls. So, Based on this here I write my abstraction which will be used to solve the problem.

## SOLUTION OVERVIEW for 1st problem:

### ABSTRACTION:
* **Step1:** Statespace is all the possible paths that one can take from the given pichu location inorder to reach the goal node(@).
* **Step2:** intial node(So) is the position where the current pichu locates at which is know from the house_map that is taken as input (pichu_loc).
* **Step3:** Successor function (SUCC:S)-> This function would tell us how to navigate through the path by passing to the next coordinate locations which is rows, columns, upper and lower diagnols. In this case, its the move function "moves(map, row, col)"
* **Step4:** Goal State: In this problem statement, we have only one goal which is the location(coordinate) of '@' to which we navigate in the optimal path.
* **Step5:** Cost Function: In a given situation, the pichu can move only in any one of the 4 directions(L,R,U,D). The cost will be 1 at each move, so the cost path would be the length of the path.(considering cost 1 for every move).

## Algorithm I have Implemented:
So, the given problem runs in to an infinite loop as there is no proper track of visited nodes and the data structure used here is stack for the implementation of DFS which is not always complete and optimal. 

Here I have implemented the BFS algorithm for the same problem and using the Queue data structure for the fringe which is FIFO. 

The steps followed are: 
Input is the map. Start from the pichu_loc and traverse to the next possible node which is solved by the successor function and also store the previous location so that the path can be remembered. eventually, once the @ is reached we output the current distance and also traverse back to get the optimal path.


## Question2:
This problem statement is follow up from the 1st one. That is given a map which has pichus>=1 and we need to find how many more pichus can be placed in the same map so that the constraints stay intact. 

## Solution Overview for the 2nd problem:

## ABSTRACTION:
* **Step1:** Statespace is all the possible maps (states) through which we place pichus in all valid locations possible until that map.
* **Step2:** Initial State is the map which has pichus>=1 based on the initial_house_map(input). 
* **Step3:** Successor function (SUCC:S)-> successors(house_map) is the function which takes the initial_house_map and returns the next valid positions in the map to place the pichu optimally. 
* **Step4:** Goal State: The final house_map which has all k pichus been placed in the valid positions so that the constraints are satisfied. Here k>=1 which is taken as input.
* **Step5:** Cost Function: Everytime we place a pichu, I consider the cost of placing it at that position is 1 as I have already got the valid positions to place the pichus. 

## Algorithm I have implemented:
Here as the given code tries to implemenent DFS and it doesn't contradict with the infinite loop as we don't keep track of visited nodes as in the problem1.

The Steps followed are:
The Input is intial_house_map and K>=1. Here I have created 2 functions. 
is_validrc(house_map,r,c) which traverse through all the rows and columns and check if a particular location is valid and place a * in that and it checks for certain patterns where the pichus can be placed and return the boolean.
is_validdiag(house_map,r,c) which has divided the diagnols in to the upper and lower right as well as upper and lower left and check all the possible directions and returns the boolean if the pichus can be placed or not.
Finally, the outputs of these are added together and return the final boolean which tells us where to place the pichu.





