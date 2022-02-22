import math
import os
import numpy as np
import pandas as pd


class Matrix:
    """
    Obtaining distance matrix from file.

    Note: It would be memory and resource efficient to compute and store (N+1)⋅N/2 elements instead of a matrix of N2.
    This would be possible due to the properties of the symmetric matrix. But let's keep it simple by computing the
    whole matrix.
    """

    @classmethod
    def load_file(cls, path_file):
        if not os.path.isfile(path_file):
            raise "file does not exist"

        dataframe = pd.read_csv(path_file, header=None)

        if len(dataframe) == 0:
            raise "Error loading the dataframe"

        return dataframe

    @classmethod
    def get_coordinates_list(cls, dataframe=None, path_file=''):
        if dataframe is None and path_file:
            dataframe = cls.load_file(path_file=path_file)

        cities_coordinates = []

        x_list = dataframe[0].to_list()
        y_list = dataframe[1].to_list()

        for i in range(dataframe.shape[0]):
            city = [x_list[i], y_list[i]]
            cities_coordinates.append(city)

        return cities_coordinates

    @classmethod
    def generate_matrix(cls, dataframe=None, path_file=''):
        """
        Create the distance matrix given a list of coordinates of each city
        """
        if dataframe is None and path_file:
            dataframe = cls.load_file(path_file=path_file)

        coord_list = cls.get_coordinates_list(dataframe=dataframe)
        num_of_cities = len(coord_list)
        matrix = np.zeros(shape=(num_of_cities, num_of_cities))

        for i in range(num_of_cities):
            for j in range(num_of_cities):

                dist = cls.get_dist_two_nodes(coord_list, i, j)

                if i == j:
                    continue

                matrix[i][j] = dist

        return matrix

    # functional method
    @staticmethod
    def get_dist_two_nodes(coord_list, node_1, node_2):
        """
        Get the relative distance by applying the Pythagorean theorem
        """
        x1 = coord_list[node_1][0]
        y1 = coord_list[node_1][1]
        x2 = coord_list[node_2][0]
        y2 = coord_list[node_2][1]

        dist = math.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

        return dist
