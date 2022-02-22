from abc import ABCMeta, abstractmethod
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
