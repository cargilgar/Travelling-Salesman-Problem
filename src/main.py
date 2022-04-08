import sys
import argparse
import inspect
from itertools import cycle

from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
from hill_climbing import HillClimbing


class ArgumentParser:
    """
    Argument parser for the commands input to solve the TSP
    """
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Solve the Travelling Salesman Problem (TSP)',
            usage='''python main.py <algorithm> [<args>]'
            These arguments are required to solve TSP:
            algorithm      Algorithm to choose from the already available.
            ''')

        parser.add_argument('algorithm', help='Choose algorithm. Refer to docs for more information')

        args = parser.parse_args(sys.argv[1:2])

        getattr(self, args.algorithm)()

    @classmethod
    def run_tsp_solver(cls, algorithm, args):
        tsp_solver = algorithm(**args)
        tsp_solver.run()

    @classmethod
    def get_algorithm_args(cls, algo_select):
        parser = argparse.ArgumentParser(description=algo_select.__doc__)

        constructor_args_dict = dict(zip(inspect.getfullargspec(algo_select.__init__).args[1:],
                                         inspect.getfullargspec(algo_select.__init__).defaults))

        for arg, default in constructor_args_dict.items():
            parser.add_argument('--' + arg, action='store_true', help=str(default))

        known_args, unknown_args = parser.parse_known_args(sys.argv[2:])

        known_args_dict = vars(known_args)
        input_args = cycle(unknown_args)
        constructor_args = {}

        for key, value in known_args_dict.items():
            res = next(input_args) if value else constructor_args_dict[key]

            try:
                constructor_args[key] = int(res)
            except ValueError:
                constructor_args[key] = res

        cls.run_tsp_solver(algo_select, constructor_args)

    @classmethod
    def sa(cls):
        cls.get_algorithm_args(SimulatedAnnealing)

    @classmethod
    def ts(cls):
        cls.get_algorithm_args(TabuSearch)

    @classmethod
    def ga(cls):
        cls.get_algorithm_args(GeneticAlgorithm)

    @classmethod
    def hc(cls):
        cls.get_algorithm_args(HillClimbing)


if __name__ == "__main__":
    MIN_VERSION = (3, 8)
    if not sys.version_info >= MIN_VERSION:
        sys.exit(
            f'Minimum Python {MIN_VERSION[0]}.{MIN_VERSION[1]} is required. Your current version is: {sys.version}')

    ArgumentParser()
