import csv
import math
import numpy as np

from ..definitions.definitions import get_abs_path


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
    def load_file(cls, file):
        """
        Load the given csv file. It should be located in the data folder.
        :returns: list of coordinates of each city
        """

        path_file = get_abs_path('data', file)

        cities_coordinates = []
        try:
            with open(path_file, 'r', encoding='utf-8') as in_file:
                reader = csv.reader(in_file, quoting=csv.QUOTE_NONNUMERIC)

                for row in reader:
                    cities_coordinates.append(row)
        except FileNotFoundError as err:
            raise err

        assert len(cities_coordinates) > 0, "Error loading the csv file"

        return cities_coordinates

    def generate_matrix(self):
        """
        Create the distance matrix given a list of coordinates of each city.

        Note: It would be resource efficient to compute and store (N+1)⋅N/2 elements instead of a matrix of N2.
        This would be possible due to the properties of the symmetric matrix. But let's keep it simple by computing the
        whole matrix.

        :returns: distance matrix
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
        Get the relative distance by applying the Pythagorean theorem.

        :returns: distance between two points
        """
        x_node_1 = coord_list[node_1][0]
        y_node_1 = coord_list[node_1][1]
        x_node_2 = coord_list[node_2][0]
        y_node_2 = coord_list[node_2][1]

        dist = math.sqrt(pow((x_node_1 - x_node_2), 2) + pow((y_node_1 - y_node_2), 2))

        return dist

    @staticmethod
    def generate_random_search_space(nodes=25):
        """
        Generate a randomly generated search space given the number of nodes.
        :returns: list of coordinates of each node (city)
        """
        np.random.seed(42)

        coord = []
        for _ in range(nodes):
            x_node = np.random.uniform(0, 100)
            y_node = np.random.uniform(0, 100)
            coord.append([x_node, y_node])

        return coord
