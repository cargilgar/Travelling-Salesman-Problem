import math
import os
import numpy as np
import csv


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

        cities_coordinates = []
        with open(path_file, 'r') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)

            for row in reader:
                cities_coordinates.append(row)

        if len(cities_coordinates) == 0:
            raise "Error loading the csv file"

        return cities_coordinates

    @classmethod
    def get_coordinates_list(cls, path_file):
        return cls.load_file(path_file)

    @classmethod
    def generate_matrix(cls, coord_list=None, path_file=''):
        """
        Create the distance matrix given a list of coordinates of each city
        """
        if coord_list is None and path_file:
            coord_list = cls.load_file(path_file=path_file)

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
