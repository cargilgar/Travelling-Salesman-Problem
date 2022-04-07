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
        self.matrix = matrix.Matrix(path)
        self.x_coord, self.y_coord = zip(*self.matrix.coord_list)

        self.x_min, self.x_max = min(self.x_coord), max(self.x_coord)
        self.y_min, self.y_max = min(self.y_coord), max(self.y_coord)

        self.nodes = len(self.matrix.matrix[0])
        self.stop = stop
        self.n_op = n_ops.get_operator_by_name(n_op)

        self.cycles = 0

    @abstractmethod
    def run(self):
        """
        Run the algorithm until the stopping criterion is met.
        """
        pass

    def generate_init_candidate(self, random_init=True):
        init_solution = []
        if random_init:
            init_solution = random.sample(range(0, self.nodes), self.nodes)
        else:
            # TODO: greedy start
            pass

        assert len(set(init_solution)) == self.nodes, 'The randomly generated initial solution does not contain all ' \
                                                      'the {} items'.format(self.nodes)
        return init_solution

    def evaluate_solution(self, tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += self.matrix.matrix[tour[i]][tour[i + 1]]

        # adding the cost from last city in the route to the starting city
        cost += self.matrix.matrix[tour[-1]][tour[0]]

        return cost

    def plot_path(self, tour, title='', subtitle=''):
        """
        Plot the given path of nodes to visualise the result.
        """
        plt.xlim(self.x_min - self.x_max * 0.1, self.x_max + self.x_max * 0.1)
        plt.ylim(self.y_min - self.y_max * 0.1, self.y_max + self.y_max * 0.1)

        plt.scatter(self.x_coord, self.y_coord, color='black')

        path_x = [self.x_coord[val] for val in tour]
        path_y = [self.y_coord[val] for val in tour]

        # adding the last city to come back to the starting point
        path_x.append(path_x[0])
        path_y.append(path_y[0])

        plt.suptitle(title, fontsize=16)
        plt.title(subtitle, fontsize=14)

        plt.plot(path_x, path_y, color='green')

    def plot_search_space(self, title='', subtitle=''):
        plt.rcParams["figure.figsize"] = (10, 8)
        plt.tight_layout()
        plt.xlim(self.x_min - self.x_max * 0.1, self.x_max + self.x_max * 0.1)
        plt.ylim(self.y_min - self.y_max * 0.1, self.y_max + self.y_max * 0.1)

        plt.suptitle(title, fontsize=16)
        plt.title(subtitle, fontsize=14)

        plt.scatter(self.x_coord, self.y_coord, color='black')
        plt.show()

    @staticmethod
    def plot_convergence(costs_list, title, x_label='', y_label=''):
        plt.suptitle(title, fontsize=16)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        plt.plot(costs_list)
        plt.show()
