# a2
**Team** : Chandra Sagar Bhogadi(cbhogadi@iu.edu), Bhavik Kollipara(srikoll@iu.edu), Brendan Mcshane(bmcshane@iu.edu).


## Part-1 (Raichu)

* Raichu is a board game played in alternate turns. There are 3 pieces in total. The board contains Pichus(White and Black), Pikachus( White and Black) and eventually both becomes raichus(White, Black) when they reach the opposite end of the board. every piece has its own rules on which it can make moves.

*  **Initial State** : It will be a (N * N) Board with 2nd row consists of white pikachus and in the alternative columns of 3rd row consists of white pichus. And on n-1th row,it has Black pikachus, alternate columns of n-2th row has Black pichus.


*  **Statespace** : All the possible states on the board we arrive at based on the moves made by pichus and pikachus provided they follow the rules of the game board.


*  **Successor Function** : Every piece has has to make a single valid move based on any of the pieces(Pichu, Pikachu and Raichu) on the board of the respective   player's colour.


   Pichu moves: Moves diagonally forward if the next square is empty. It can jump over only pichu's of the opposite colour.

   Pikachu Moves: Moves one or two steps either forward,left or right, if the next square is empty. It can Jump over the opposite colour of pichu/pikachus.

   Raichu Moves: It is created when pichu or pikachu reaches opposite side of the board. It can jump over opposite colour of either pichu,pikachu or Raichu and land                  any number of steps forward provided there are empty squares between Raichu and jumped piece.

   In all the cases, the jumped piece is removed as soon as it is jumped over.

*  **Cost Function/Static Evaluation Function**  : Here, there isn't any cost function as such, but we use our static evaluation function to back track the minimax tree of states to evaluate which states to choose and also implement alpha-beta pruning.


*  **Goal State** : The board containing pieces of one of the colour more than the other pieces or equal (draw) until the program's time-out.


## Part-2 (Qunitris Game) 
So I think what I'm going to try to do is have an algorithm that's based off of how many holes are left under the piece when it falls into place. Ideally there's zero and every space underneath the piece that's falling is either the bottom of the game board or part of another piece, and we have no empty space underneath the current piece. The less holes the better, essentially. From there I can prioritize locations that are lower down on the game board and also the completion of rows, but maybe those end up kinda being the same thing. In any case, I need to test out (4 positions * width of the board) possible placements of each piece. I might check if a piece is symmetric to cut down on that which will come in handy later in the game when we don't have a lot of time to make decisions. As it turns out the horizontal flip changes the whole orientation so I'll have (8 positions * width of the board) possible placements for each piece.

So I think I'm going to implement a cost function that checks the:
1) number of holes and partial holes on the board
2) the overall bumpiness of the floor
3) the height of the piece in it's current orientation

and I'm going to calculate the cost of dropping the current piece in all of the possible locations that I can drop it, and then going with the column and orientation that minimizes the cost. The tricky part is going to be coming up with competent weights for each of the attributes of the cost function and also simulating the piece falling in with that specific configuration.

I've had bugs that I've had a hard time figuring out for the last couple days, my game would stop immediately before any pieces were dropped and it would either not give me any error to work with or every 5 or 6 times I'd get a weird threading error that also wasn't helpful. This made debugging quite difficult, the only reason I was able to figure out some of the earlier bugs was because on the ~20th attempt at running the same script over and over again an error popped up and I was able to fix it and get things running temporarily when I stopped in at office hours and got it figured out. Unfortunately I'm running out of time to code a fix so in case it doesn't work when you guys run it you'll know why.

My algorithm essentially tries to accomplish the following
For each piece as soon as it starts falling:
    Look at every combination of piece orientation + column and calculate the cost via
        cost = weight1 * number of holes + weight2 * number of partial holes + weight3 *bumpiness of floor (floor here is the highest 'x' in each column, bumpiness is the sum of the differences from each column to the next. The flatter our floor is and the more horizontal all of our pieces are and the more likely we are to be completing rows and avoiding the ceiling. Holes make completing rows much more difficult)

    choose the orientation that's the cheapest
    repeat



I managed to fix the bug, I just changed the way I was checking if the piece was done falling or not. However now all of my pieces are cramming themselves on the left side of the screen and building as tall as they can, almost the exact opposite of what I'm trying to do. The pieces are rarely flipping/rotating as well, so I wonder if each time my algorithm just picks the first available option for piece orientation and column (which would be no flips and leftmost column) and runs with it. Also, whenever the game ends for both simple and animated I don't get returned to the prompt for the terminal, and when I ctrl+c to interrupt the process with my kepboard I'll get weird errors in QuintrisGame.py.

## Part-3 (Seeking Truth)


* Naive Bayes is a classification algorithm that works based on the Bayes theorem.

* Bayes Theorem : P(A/B)=P(B/A)*P(A)/P(B)

* In this, using Bayes theorem we can find the probability of A, given that B occurred. A is the hypothesis and B is the evidence.
* P(B|A) is the probability of B given that A is True.
* P(A) and P(B) is the independent probabilities of A and B.
**TASK-**  classify reviews into faked or legitimate for 20 hotels in Chicago.
**Given -** data set of user generated reviews ( training and test data )

* Let the two classes into which the reviews have to be categorized be A and B

Where A- truthful and B - deceptive

P(A/W1,W2,W3,.....Wn) = P(W1,W2....Wn/A)*P(A)/P(W1,W2,W3,...Wn)
P(B/W1,W2,W3,.....Wn) = P(W1,W2....Wn/B)*P(B)/P(W1,W2,W3,...Wn)

* where

P(A/W1,W2,W3,.....Wn) , P(B/W1,W2,W3,.....Wn) - Posterior Probability

P(W1,W2....Wn/A) ,  P(W1,W2....Wn/B)  -  Likelihood

by naive bayes assumption

P(W1,W2....Wn/A) = P(W1/A)*P(W2/A)*P(W3/A)........P(Wn/A)

P(W1,W2....Wn/B) = P(W1/B)*P(W2/B)*P(W3/B)........P(Wn/B)

* P(A) , P(B) - prior probability
* P(W1,W2,W3,...Wn) -  marginal likelihood


**Step-1**
Convert the user generated reviews into bag of words model

**Step-2**
Find all the probabilities required for the Bayes theorem for the calculation of posterior probability
(we created a dictionary with keys as unique words and values as the posterior probabilities for each word )

**Step-3**
compare the posterior probabilities
i.e if P(A/W1,W2,W3,.....Wn) / P(B/W1,W2,W3,.....Wn) >1 classify the review into category A(truthful) else classify it into category B (deceptive).
