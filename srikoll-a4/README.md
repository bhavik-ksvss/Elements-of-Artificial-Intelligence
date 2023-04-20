# a4

## Part 1. K-nearest-neighbours

**Goal:** To Implement KNN algorithm from scratch for both Iris and Digits Dataset and compare results to sklearn implemented.

* Here we need to implement four functions which are eucledian_distance,manhattan_distance,fit and predict.
* Eucledian distance (L2 norm) is the shortest distance between two points in an N-dimensional space.
* Manhattan distance (L1 norm) is a distance metric between two points in a N dimensional vector space. It is the sum of the lengths of the projections of the line segment between the points onto the coordinate axes.
* Fit method here used to fit the KNN algorithm to the given new dataset (X,y)
* KNN is a Non-linear, Non-Parametric and Supervised algorithm used for both Classification and Regression Tasks.
* KNN, in a higher level view classifies a new data-point based on it's nearest neighbours.
* There arise two different cases here, where in weights can be either 'uniform' or 'distance'
* When the weights are equal to uniform, all the nearest neighbours are taken in to consideration,the class with majority vote is the label for the new data-point.
* When the weights are equal to distance, the weights to each neighbour is inversely proportional to it's distance from the data-point for which the label needs to be classified.
* Achieved very good accuracies as compared to sklearn model.
* The accuracy scores achieved on the two given datasets can be found in the html files uploaded.


## Part 2. Multi-layer Perceptron

**Goal:** To Implement a feedforward fully-connected multilayer perceptron classifier with one hidden layer.

* A MLP is actually a function of many variables: It takes an input, makes computations and produces an output.
* With each neuron in a layer connected with all neurons in the previous and the next layer. All the computations take place inside those neurons and depend on the   weights that connect the neurons with each other.
* Various activation functions such as sigmoid,tanh,relu are implemented which include non-linearity in the network.
* Both the biases of hidden and output layer are set to 1 for a simple model.
* The weights in the both those layers are intialized to random values intially.
* A1 = h(W1*X + b1), A2 = g(W2*A1 + b2) are the two steps that we perform majorily here in the forward step.
* cross-entropy loss has been used here.
* Now, we perform Back propagation to update weights of both layers.
* Calculated the gradients of Loss Function and use gradient descent algorithm
* Train the Network using the updated weights for certain number of epochs.
* Now that the network has been trained, we tested this simple neural network on Iris and MNIST dataset. Achieved decent accuracies for some data points. Well, It depends on lot of Hyper-parameters.
* The accuracy scores achieved on the two given datasets can be found in the html files uploaded.
