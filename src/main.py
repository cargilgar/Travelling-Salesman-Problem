import matplotlib.pyplot as plt
import sys
import argparse
import inspect
import itertools
import re

from genetic_algorithm import GeneticAlgorithm
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch
from hill_climbing import HillClimbing

algorithms = {
    'sa': SimulatedAnnealing(),
    'ts': TabuSearch(),
    'ga': GeneticAlgorithm(),
    'hc': HillClimbing()
}


def plot_convergence(costs_list, title, x_label='', y_label=''):
    plt.suptitle(title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.plot(costs_list)
    plt.show()


class ArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Solve the Travelling Salesman Problem (TSP)',
            usage='''python main.py <algorithm> [<args>]'
            These arguments are required to solve TSP:
            algorithm      Algorithm to choose from the already available.
            --file         CSV file containing coordinates of each node.
            ''')

        parser.add_argument('--file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                            help='CSV file containing coordinates of each node')

        parser.add_argument('algorithm', help='Choose algorithm. Refer to docs for more information')

        args = parser.parse_args(sys.argv[1:2])

        getattr(self, args.algorithm)()
        
    @staticmethod
    def get_algorithm_args(algo):
        parser = argparse.ArgumentParser(description=algo.__doc__)

        constructor_args_dict = dict(zip(inspect.getfullargspec(algo.__init__).args[2:],
                                    inspect.getfullargspec(algo.__init__).defaults[1:]))

        for arg, default in constructor_args_dict.items():
            print(arg, default)
            parser.add_argument('--' + arg, action='store_true', help=str(default))

        parser.parse_args(sys.argv[2:])

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

    # if not parser.args.file:
    #     file = '../TSP_50_nodes.csv'  # if no file is given, then a random search space is generated
    #
    # if args.algorithm:
    #     algo = algorithms.get(args.algorithm)
    # else:
    #     choice = input('Choose an algorithm: \n\tsa (Simulated Annealing) \n\tts (Tabu Search) \n\tga (Genetic Algorithm) \n\thc (Hill Climbing) \n')
    #     algo = algorithms.get(choice)
    #
    #     constructor_params = str(inspect.signature(algo.__init__))[10:-1]
    #     print(f'Default parameters for {algo.name}: \n\t{constructor_params}')
    #     leave_default = input('Keep these default parameters? (y/n) \n')
    #
    #     if leave_default == 'n':
    #         constructor_params = constructor_params.split(', ')
    #         # constructor_params = constructor_params[1:]
    #         default_pattern = re.compile(r'\w*(?==)')
    #         for default_param in constructor_params:
    #             param = default_pattern.search(default_param)
    #             choice = input(f'Enter value for {param[0]}: ')
    #
    #     best_costs, best_solution = algo.run(animation=True)
    #     plot_convergence(best_costs, f'{algo.name} minimisation convergence', x_label=f'Total iterations: {algo.cycles}', y_label='Cost')
    #     print('TS best solution', best_solution)
