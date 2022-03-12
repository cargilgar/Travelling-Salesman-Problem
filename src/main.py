import matplotlib.pyplot as plt
import sys
import argparse
import inspect
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


parser = argparse.ArgumentParser(description='Solve the Travelling Salesman Problem')

parser.add_argument('-f', '--file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)

parser.add_argument('-a', '--algorithm', required=False,
                    choices=['sa', 'ts', 'ga', 'hc'],
                    help='Choose algorithm. Refer to docs to see each type')

args = parser.parse_args()

if __name__ == "__main__":
    MIN_VERSION = (3, 8)
    if not sys.version_info >= MIN_VERSION:
        sys.exit(
            f'Minimum Python {MIN_VERSION[0]}.{MIN_VERSION[1]} is required. Your current version is: {sys.version}')

    if not args.file:
        file = '../TSP_50_nodes.csv'  # if no file is given, then a random search space is generated

    if args.algorithm:
        algo = algorithms.get(args.algorithm)
    else:
        choice = input('Choose an algorithm: \n\tsa (Simulated Annealing) \n\tts (Tabu Search) \n\tga (Genetic Algorithm) \n\thc (Hill Climbing) \n')
        algo = algorithms.get(choice)

        constructor_params = str(inspect.signature(algo.__init__))[10:-1]
        print(f'Default parameters for {algo.name}: \n\t{constructor_params}')
        leave_default = input('Keep these default parameters? (y/n)')

        if leave_default == 'n':
            constructor_params = constructor_params.split(', ')
            # constructor_params = constructor_params[1:]
            default_pattern = re.compile(r'\w*(?==)')
            for default_param in constructor_params:
                param = default_pattern.search(default_param)
                choice = input(f'Enter value for {param[0]}: ')

        algo.run(True)


    # HC = HillClimbing(file, climb_type='steepest')
    # iterations, best_costs, best_solution = HC.run(animation=True)
    # plot_convergence(best_costs, 'Hill climbing minimisation convergence', x_label=f'Total iterations: {iterations}',
    #                  y_label='Cost')
    # print('Hill climbing best solution', best_solution)

    # # --- Testing Simulated Annealing with inversion operator
    # SA = SimulatedAnnealing(file, operator='rand_swap', t_max=40, t_min=0, alpha=0.998)
    # iterations, best_costs, best_solution = SA.run(animation=True)
    #
    # # SA accepts bad moves so this will plot a fluctuating descending curve. Also, because the probability acceptance
    # # decreases over time, the curve will present bigger fluctuations at the beginning and less at the end.
    # plot_convergence(best_costs, 'SA minimisation convergence', x_label=f'Total iterations: {iterations}', y_label='Cost')
    # print('SA best solution', best_solution)
    #
    # # --- Testing Tabu Search with inversion operator
    # TS = TabuSearch(file, operator='inversion', tabu_size=20, stop=1000)
    # iterations, best_costs, best_solution = TS.run(animation=True)
    # plot_convergence(best_costs, 'TS minimisation convergence', x_label=f'Total iterations: {iterations}', y_label='Cost')
    # print('TS best solution', best_solution)
    #
    # # --- Running GA with tuned parameters
    # GA = GeneticAlgorithm()
    # iterations, best_costs, best_solution = GA.run(animation=True)
    # plot_convergence(best_costs, 'Evolution GA tuned parameters', x_label=f'Total iterations: {iterations}', y_label='Cost')
    # print('GA best solution', best_solution)
