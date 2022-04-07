import matplotlib.pyplot as plt

from algorithm import Algorithm


class TabuSearch(Algorithm):
    """Tabu Search Algorithm"""
    def __init__(self, file='', stop=100, operator="rand_swap_adj", tabu_size=20):
        super().__init__(file, stop, operator)
        self.tabu_tenure = tabu_size
        self.tabu_list = []

    def run(self):
        """
        Run the Tabu Search algorithm to stop when...
        The algorithm generates candidates based on the selected neighbourhood
        operator and will tend to accept less bad moves over time,
        according to the acceptance probability.
        """
        print(f'\nRunning {self.__doc__}. Stopping if no improvement after {self.stop} iterations \n')
        best_solution = self.generate_init_candidate()
        best_cost = self.evaluate_solution(best_solution)
        cost_best_candidate = best_cost
        cost_candidates = [best_cost]

        plt.rcParams["figure.figsize"] = (10, 8)
        plt.tight_layout()

        count, self.cycles = 0, 0
        while count < self.stop:
            sol_best_candidate = self.n_op.generate_candidate_solution(best_solution.copy())
            # Evaluate all possible solutions within the neighbourhood space
            tabu_move = []
            for i in range(len(sol_best_candidate) - 1):
                solution_candidate = sol_best_candidate.copy()
                solution_candidate[i], solution_candidate[i + 1] = solution_candidate[i + 1], solution_candidate[i]

                if tabu_move not in self.tabu_list and \
                        (cost_candidate := self.evaluate_solution(solution_candidate)) < cost_best_candidate:
                    sol_best_candidate = solution_candidate.copy()
                    cost_best_candidate = cost_candidate
                    tabu_move = [solution_candidate[i], solution_candidate[i + 1]]

            if cost_best_candidate < (best_cost := self.evaluate_solution(best_solution)):
                best_solution = sol_best_candidate.copy()
                cost_candidates.append(best_cost)
                self.cycles += 1
                count = 0

                plt.cla()
                self.plot_path(best_solution, f'{self.__doc__} using {self.n_op.name}',
                               f'Iteration: {self.cycles} \nCost: {round(cost_candidates[-1])}')
                plt.pause(0.05)

                self.tabu_list.append(tabu_move)

            # Updating the tabu list so that old tabu moves can be accepted again
            if len(self.tabu_list) > self.tabu_tenure:
                self.tabu_list.pop(0)

            count += 1

        plt.show(block=True)

        self.plot_convergence(cost_candidates, f'{self.__doc__} minimisation convergence',
                              x_label=f'Total iterations: {self.cycles}', y_label='Cost')
