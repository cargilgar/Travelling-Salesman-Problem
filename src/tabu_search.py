import matplotlib.pyplot as plt

from algorithm import Algorithm


class TabuSearch(Algorithm):
    def __init__(self, file, stop=100, operator="rand_swap_adj", tabu_size=20):
        super().__init__(file, stop, operator)
        self.tabu_tenure = tabu_size
        self.tabu_list = []

    def run(self, animation=False):
        """
        Run the Tabu Search algorithm to stop when...
        The algorithm generates candidates based on the selected neighbourhood
        operator and will tend to accept less bad moves over time,
        according to the acceptance probability.
        """
        print(f'\nRunning Tabu Search. Stopping if no improvement after {self.stop} iterations')
        best_solution = self.generate_init_candidate(self.nodes)
        best_cost = self.evaluate_solution(best_solution)
        cost_best_candidate = best_cost
        cost_candidates = [best_cost]

        if animation:
            plt.rcParams["figure.figsize"] = (10, 8)

        count, its = 0, 0
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
                its += 1
                count = 0

                if animation:
                    plt.cla()
                    self.plot_path(self.coord, best_solution, f'Tabu Search using {self.n_op.name}',
                                   f'Iteration: {its} \nCost: {round(cost_candidates[-1])}')
                    plt.pause(0.05)

                self.tabu_list.append(tabu_move)

            # Updating the tabu list so that old tabu moves can be accepted again
            if len(self.tabu_list) > self.tabu_tenure:
                self.tabu_list.pop(0)

            count += 1

        if animation:
            plt.tight_layout()
            plt.show()

        return its, cost_candidates, best_solution
