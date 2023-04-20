# a1-forrelease

# Report

Report

Elements of Artificial Intelligence

## Part 1 : 2021 Puzzle

Initial State: Board in a disarranged manner.

Heuristic used : Manhattan Distance is used to compare the disarranged board and the correctly arranged board.

Goal State : A properly arranged board with 1 ….25

Successor function : The next available move with the least Manhattan Distance

How we worked on the problem : After finding the Manhattan distance for each tile, total Manhattan distance was calculated. 24 moves can be made in total. The tile with the minimum Manhattan distance is selected and this goes on till we reach zero else we backtrack and the process continues.

The branching factor of the tree is 24 as maximum of 24 moves can be made

If the solution can be reached in 7 moves, we would need to explore 24^7 moves before we found if we used BFS instead of A* search .

## Part-2 : Road Trip
The first task involves reading two data sets citygps.txt which contains the lattitude and longitude of the cities and roadsegments.txt which contains a road connecting two cities along with path length in miles ,speed limit and highway name .All roads given in roadsegments.txt are biredctional . For this we created a dictionary which contains name of the city as the key and values as the cities which are connected to the (key-city).Like real world data this data contains some bugs ie not all cities that appear in road-segments.txt
have a corresponding line in city-gps.txt but our code must accept it as an exception and run without any interuption .  

The problem is to find a path connecting two places according to the given cost function. The cost functions mentioned are distance,speed,time,delivery-time
We used A* search alogorithm to find the optimal path and implemented this with a priority queue. The priority queue was implemented from scratch and it returns the element with highest priority when 'pop' command is used. 
We added a list named 'Visited' to check if a city is already visited , if it is visited then it is not pushed into the queue again.
If the speed limit of the road is greater than 50 the delivery time becomes troad+2*p(troad+trip) ,so we check when if speed is greater than 50 and proceed accordingly.
When cost function is -
--Distance--
We used haversines formula as the heuristic function to estimate the distance between two cities and if the latitide and longitue of a city is not available we calcualted the distance as - (distance between start city and end city - distance travelled until then ) this always underestimates the actual cost as it is a admissible heuristic.
--Time-- 
The heuristic here is Distance calculated from haversines function divided by the speed and if the latitide and longitue of a city is not available we calcualted the time as 
(distance between start city and end city - distance travelled until then )/maximum speed in the whole map ,this always underestimates the actual cost as it is a admissible heuristic
--Delivery Time--
We used the same method of implementation as for time cost function 


The first element of the queue is poped which has all the details of the path traversed till that node. If the of a node is the destination then it returns the path,distance,time,delivery-time and length of path .If no path exists between the given two cities 'cant find path' is returned .


## Part-3: Choosing Teams
In this problem, we need to find the best teammates possible for the students based on their group preferences with the constraints apply and in the minimal possible complaints cost. So, the solution should be such that the complaint cost of creating a team need to be less than the threshold value.

Initial State: The individual students are treated as the default team.

State space: Every time we try to randomize the one of the team members to other team, it’s the state space.

Cost Function: Every time, we have a cost of 1 for changing the member from one team to other.

Goal State: The set of teams which require the minimum amount of instructor’s time in grading and complaint cost.

Heuristic: Every iteration randomizing the teams, we get new set of teams. Whenever we have minimum computed complaint cost, we yield the set of teams and cost.

The Local search algorithm has been used for this problem finds the set of teams which require the minimum amount of work done by the instructor.





 
