from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import random

from utils.matrix import matrix
from utils.n_ops import n_ops


class Algorithm:
    """
    Abstract class to be inherited by TS, SA and GA. It contains basic members related to TSP.
    """
    __metaclass__ = ABCMeta

    def __init__(self, path, stop, n_op):
        self.matrix = matrix.Matrix.generate_matrix(path_file=path)
        self.nodes = len(self.matrix[0])
        self.coord = matrix.Matrix.get_coordinates_list(path_file=path)
        self.stop = stop
        self.n_op = n_ops.get_operator_by_name(n_op)

    @abstractmethod
    def run(self):
        """
        Run the algorithm until the stopping criterion is met.
        """
        pass

    @classmethod
    def generate_init_candidate(cls, items, random_init=True):
        init_solution = []
        if random_init:
            init_solution = random.sample(range(0, items), items)
        else:
            # TODO: greedy start
            pass

        assert len(set(init_solution)) == items, 'The randomly generated initial solution does not contain all ' \
                                                 'the {} items'.format(items)
        return init_solution

    def evaluate_solution(self, tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.matrix[tour[i]][tour[i + 1]]

        # adding the cost from last city in the route to the starting city
        cost += self.matrix[tour[-1]][tour[0]]

        return cost

    @staticmethod
    def plot_path(coord, tour, title, subtitle):
        """
        Plot the given path of nodes to visualise the result.
        """
        x_coord, y_coord = [], []

        for item in coord:
            x_coord.append(item[0])
            y_coord.append(item[1])

        path_x, path_y = [], []

        for val in tour:
            path_x.append(x_coord[val])
            path_y.append(y_coord[val])

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(path_x, path_y, color='black')

        plt.suptitle(title, fontsize=16)
        plt.title(subtitle, fontsize=14)

        # adding the last city to come back to the starting point
        path_x.append(path_x[0])
        path_y.append(path_y[0])

        plt.plot(path_x, path_y, color='green')
