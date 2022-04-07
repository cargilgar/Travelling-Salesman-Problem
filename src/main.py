import sys
import argparse
import inspect

from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
from hill_climbing import HillClimbing


class ArgumentParser:
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

        known_args, unknown = parser.parse_known_args(sys.argv[2:])

        known_args_dict = vars(known_args)

        constructor_args = dict()

        for i, (key, value) in enumerate(known_args_dict.items()):
            if value:
                try:
                    constructor_args[key] = int(unknown[i])
                except ValueError:
                    constructor_args[key] = unknown[i]
            else:
                try:
                    constructor_args[key] = int(constructor_args_dict[key])
                except ValueError:
                    constructor_args[key] = constructor_args_dict[key]

        cls.run_tsp_solver(algo_select, constructor_args)

    def sa(self):
        self.get_algorithm_args(SimulatedAnnealing)

    def ts(self):
        self.get_algorithm_args(TabuSearch)

    def ga(self):
        self.get_algorithm_args(GeneticAlgorithm)

    def hc(self):
        self.get_algorithm_args(HillClimbing)


if __name__ == "__main__":
    MIN_VERSION = (3, 8)
    if not sys.version_info >= MIN_VERSION:
        sys.exit(
            f'Minimum Python {MIN_VERSION[0]}.{MIN_VERSION[1]} is required. Your current version is: {sys.version}')

    ArgumentParser()
