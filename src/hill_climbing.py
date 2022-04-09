import matplotlib.pyplot as plt

from algorithm import Algorithm


class HillClimbing(Algorithm):
    """Hill Climbing Algorithm"""
    def __init__(self, file='', stop=20, operator="inversion", climb_type='steepest'):
        super().__init__(file, stop, operator)
        self.climb_type = climb_type

        self.evaluate = {
            'steepest': self.evaluate_neighbourhood_space,
            'ascent': self.evaluate_solution
        }

    def evaluate_neighbourhood_space(self, tour):
        """
        Steepest Ascend only: Evaluate all possible solutions within the neighbourhood space and select the best one.
        """
        cost = self.evaluate_solution(tour) * 10  # this makes a number big enough to hit the first condition
        best_candidate_solution = tour.copy()

        for i in range(len(tour) - 1):
            candidate = tour.copy()
            candidate[i], candidate[i + 1] = candidate[i + 1], candidate[i]

            cost_candidate = self.evaluate_solution(candidate)

            if cost_candidate < cost:
                cost = cost_candidate
                best_candidate_solution = candidate.copy()

        # Modifying the original tour by ref
        tour[:] = best_candidate_solution

        return cost

    def run(self):
        """
        Run the Hill Climbing algorithm.
        """
        print(f'\nRunning {self.__doc__}. Stopping if no improvement after {self.stop} iterations \n')
        best_solution = self.generate_init_candidate()
        best_cost = self.evaluate_solution(best_solution)
        cost_candidates = [best_cost]

        plt.rcParams["figure.figsize"] = (10, 8)
        plt.tight_layout()

        count = 0
        while count < self.stop:
            solution_candidate = self.n_op.generate_candidate_solution(best_solution.copy())

            cost_candidate = self.evaluate[self.climb_type](solution_candidate)

            # # Evaluate solution depending on steepest ascend or simple hill climbing
            # if self.climb_type == 'steepest':
            #     solution_candidate, cost_candidate = self.evaluate_neighbourhood_space(solution_candidate)
            # else:
            #     cost_candidate = self.evaluate_solution(solution_candidate)

            if cost_candidate < best_cost:
                best_solution = solution_candidate.copy()
                best_cost = cost_candidate
                cost_candidates.append(cost_candidate)
                count = 0

            plt.cla()
            self.plot_path(best_solution, f'{self.__doc__} using {self.n_op.__doc__}',
                           f'Iteration: {self.cycles} \nCost: {round(cost_candidates[-1])}')
            plt.pause(0.05)

            self.cycles += 1
            count += 1

        plt.show(block=True)

        self.plot_convergence(cost_candidates, f'{self.__doc__} minimisation convergence',
                              x_label=f'Total iterations: {self.cycles}', y_label='Cost')
