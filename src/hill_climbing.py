import matplotlib.pyplot as plt

from algorithm import Algorithm


class HillClimbing(Algorithm):
    def __init__(self, file='', stop=20, operator="two_opt", climb_type='steepest'):
        super().__init__(file, stop, operator)
        self.name = 'Hill Climbing'
        self.climb_type = climb_type

    def evaluate_neighbourhood_space(self, tour):
        """
        Steepest Ascend only: Evaluate all possible solution within the neighbourhood space and select the best one.
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

        return best_candidate_solution, cost

    def run(self, animation=False):
        """
        Run the Hill Climbing algorithm.
        """
        print(f'\nRunning {self.name}. Stopping if no improvement after {self.stop} iterations')
        best_solution = self.generate_init_candidate()
        best_cost = self.evaluate_solution(best_solution)
        cost_candidates = [best_cost]

        if animation:
            plt.rcParams["figure.figsize"] = (10, 8)
            plt.tight_layout()

        count, its = 0, 0
        while count < self.stop:
            solution_candidate = self.n_op.generate_candidate_solution(best_solution.copy())

            # Evaluate solution depending on steepest ascend or simple hill climbing
            if self.climb_type == 'steepest':
                solution_candidate, cost_candidate = self.evaluate_neighbourhood_space(solution_candidate)
            else:
                cost_candidate = self.evaluate_solution(solution_candidate)

            if cost_candidate < best_cost:
                best_solution = solution_candidate.copy()
                best_cost = cost_candidate
                cost_candidates.append(cost_candidate)
                count = 0

            if animation:
                plt.cla()
                self.plot_path(best_solution, f'{self.name} using {self.n_op.name}',
                               f'Iteration: {its} \nCost: {round(cost_candidates[-1])}')
                plt.pause(0.05)

            its += 1
            count += 1

        if animation:
            plt.show()

        return its, cost_candidates, best_solution
