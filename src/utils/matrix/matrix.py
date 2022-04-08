import csv
import math
import os
import numpy as np


class Matrix:
    """
    This class obtains a distance matrix from a csv file and stores the coordinates of each node.
    """
    def __init__(self, path_file=''):
        if len(path_file) < 1:
            self.coord_list = self.generate_random_search_space()
        else:
            self.coord_list = self.load_file(path_file)

        self.matrix = self.generate_matrix()

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

    def generate_matrix(self):
        """
        Create the distance matrix given a list of coordinates of each city.

        Note: It would be resource efficient to compute and store (N+1)⋅N/2 elements instead of a matrix of N2.
        This would be possible due to the properties of the symmetric matrix. But let's keep it simple by computing the
        whole matrix.
        """
        num_of_cities = len(self.coord_list)
        matrix = np.zeros(shape=(num_of_cities, num_of_cities))

        for i in range(num_of_cities):
            for j in range(num_of_cities):
                if i == j:
                    continue

                dist = self.get_dist_two_nodes(self.coord_list, i, j)

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

    @staticmethod
    def generate_random_search_space(nodes=25):
        np.random.seed(42)

        coord = []
        for i in range(nodes):
            x = np.random.uniform(0, 100)
            y = np.random.uniform(0, 100)
            coord.append([x, y])

        return coord
