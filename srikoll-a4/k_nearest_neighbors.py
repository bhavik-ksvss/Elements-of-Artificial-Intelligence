# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [Bhavik Kollipara] -- [srikoll@iu.edu]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff


import numpy as np
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y
        #raise NotImplementedError('This function must be implemented by the student.')

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        if self.weights=='uniform':
            predictions = []
       
            for pred_row in range(np.shape(X)[0]):
                distances = []
                for X_row in range(np.shape(self._X)[0]):
                    distance = self._distance(X[pred_row],self._X[X_row])
                    distances.append(distance)

                neighbours = self._y[np.argsort(distances)[:self.n_neighbors]]
                neighbours_bc = np.bincount(neighbours)
                prediction = np.argmax(neighbours_bc)
                predictions.append(prediction)
            #print("uniform",predictions)

            return np.array(predictions)

        elif self.weights =='distance':
            predictions = []
            for pred_row in range(np.shape(X)[0]):
                distances = []
                for X_row in range(np.shape(self._X)[0]):
                    distance = self._distance(X[pred_row],self._X[X_row])
                    distances.append(1/distance)
                neighbours = self._y[np.argsort(-np.array(distances))[:self.n_neighbors]]
                neighbours_bc = np.bincount(neighbours)
                prediction = np.argmax(neighbours_bc)
                predictions.append(prediction)
            #print("distance",predictions)

            return np.array(predictions)            
     


        #raise NotImplementedError('This function must be implemented by the student.')
### Ref:https://github.com/python-engineer/MLfromscratch/blob/master/mlfromscratch/knn.py
