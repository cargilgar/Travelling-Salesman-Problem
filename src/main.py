import sys
import argparse
import inspect

from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
from hill_climbing import HillClimbing

algorithms = {
    'sa': SimulatedAnnealing,
    'ts': TabuSearch,
    'ga': GeneticAlgorithm,
    'hc': HillClimbing
}


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

        parser.add_argument('algorithm', action='store_true', help='Choose algorithm to solve TSP. '
                                                                   'Refer to docs for more information')

        subparsers = parser.add_subparsers(description='Sub description', dest='algo_select')

        # Creating a subparser por each algorithm, adding the arguments from the corresponding constructor
        for key, value in algorithms.items():
            subparser = subparsers.add_parser(key, help=value.__doc__)
            self.get_algorithm_args(subparser, value)

        # Getting the attributes for the main parser and the subparser selected.
        args = parser.parse_args()
        args_dict = vars(args)

        # Extracting the first two elements of args_dict to get the constructor_args
        constructor_args = dict(list(args_dict.items())[2:])

        self.run_tsp_solver(algorithms.get(args.algo_select), constructor_args)

    @staticmethod
    def run_tsp_solver(algorithm, args):
        """
        Run the algorithm given the type of algorithm and its constructor arguments
        """
        tsp_solver = algorithm(**args)
        tsp_solver.run()

    @staticmethod
    def get_algorithm_args(parser, algo_select):
        """
        Get constructor arguments from the selected algorithm.
        """
        constructor_args_dict = dict(zip(inspect.getfullargspec(algo_select.__init__).args[1:], inspect.getfullargspec(algo_select.__init__).defaults))

        for arg, default in constructor_args_dict.items():
            if isinstance(default, int):
                parser.add_argument(f'--{arg}', action='store', help=str(default), type=int, default=default)

            else:
                parser.add_argument(f'--{arg}', action='store', help=str(default), default=default)


if __name__ == "__main__":
    MIN_VERSION = (3, 8)
    if not sys.version_info >= MIN_VERSION:
        sys.exit(
            f'Minimum Python {MIN_VERSION[0]}.{MIN_VERSION[1]} is required. Your current version is: {sys.version}')

    ArgumentParser()
