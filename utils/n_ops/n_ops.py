from abc import ABCMeta, abstractmethod
import random


def get_operator_by_name(op_name):
    ops_dict = {'rand_swap': RandomSwap(),
                'rand_swap_adj': RandomSwapAdjacent(),
                'inversion': Inversion(),
                'two_opt': TwoOpt(),
                'three_opt': ThreeOpt()
                }
    return ops_dict.get(op_name)


# TODO: Lin-Kernighan, 3-opt, position-based neighbourhood (insertion)

class Operator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_candidate_solution(self, path: list) -> list:
        """
        Given a list, generate a candidate solution based on the operator type.
        """
        pass

    # functional methods
    @classmethod
    def get_random_index(cls, range_list, num_indexes):

        if num_indexes == 0:
            raise 'The number of indexes cannot be 0. It must be 1 or greater.'
        elif num_indexes == 1:
            return random.randrange(range_list)

        if num_indexes > range_list:
            raise 'More indexes to return than the size of current list.'

        ret = [random.randrange(range_list)]

        for i in range(num_indexes - 1):
            next_rand_node = random.randrange(range_list)

            # Ensure that next_rand_node is not the same as the other random nodes generated
            while next_rand_node in ret:
                next_rand_node = random.randrange(range_list)

            ret.append(next_rand_node)

        return ret

    @classmethod
    # Initial solution
    def generate_init_candidate(cls, items, random_init=True):
        init_solution = []
        if random_init:
            init_solution = random.sample(range(0, items), items)
        # TODO
        # else:
        # greedy start

        assert len(set(init_solution)) == items, 'The randomly generated initial solution does not contain all ' \
                                                 'the {} items'.format(items)
        return init_solution


class RandomSwap(Operator):
    def __init__(self):
        self.name = "Random Exchange"

    def generate_candidate_solution(self, path):
        """
        Exchange two randomly selected (not necessarily adjacent) nodes.
        """
        node_a, node_b = self.get_random_index(len(path), 2)

        path[node_a], path[node_b] = path[node_b], path[node_a]

        return path


class RandomSwapAdjacent(Operator):
    def __init__(self):
        self.name = "Random Exchange Adjacent"

    def generate_candidate_solution(self, path):
        """
        Exchange two randomly selected adjacent nodes.
        """
        node_a = self.get_random_index(len(path) - 1, 1)
        node_b = node_a + 1

        path[node_a], path[node_b] = path[node_b], path[node_a]

        return path


class Inversion(Operator):
    def __init__(self):
        self.name = "Inversion"

    def generate_candidate_solution(self, path):
        """
        Invert the sub-array contained within two randomly selected nodes.
        """
        node_a, node_b = sorted(self.get_random_index(len(path), 2))

        diff = node_b - node_a + 1

        for i in range(diff // 2):
            path[node_a + i], path[node_b - i] = path[node_b - i], path[node_a + i]

        return path


class TwoOpt(Operator):
    def __init__(self):
        self.name = "2-Opt"

    def generate_candidate_solution(self, path):
        """
        Remove randomly 2 edges and replace all the possible permutations.
        """

        node_a = self.get_random_index(len(path) - 1, 1)
        node_b = node_a + 1

        node_c = self.get_random_index(len(path) - 1, 1)

        while node_c == node_a:
            node_c = self.get_random_index(len(path) - 1, 1)

        # In 2-opt operator there are 4 possible permutations, 2 of which are the same but with opposite directions.
        # Then only one permutation is to be compared with the original path

        # Swap node_b and node_c:
        path[node_b], path[node_c] = path[node_c], path[node_b]

        return path


class ThreeOpt(Operator):
    def __init__(self):
        self.name = "3-Opt"

    def generate_candidate_solution(self, path):
        """
        Remove randomly 3 edges and replace all the possible permutations.
        """
        pass
