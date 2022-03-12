import matplotlib.pyplot as plt
import random
import math

from algorithm import Algorithm


class SimulatedAnnealing(Algorithm):
    def __init__(self, file='', stop=100, operator="rand_swap_adj", t_max=10, t_min=0.0005, alpha=0.995):
        super().__init__(file, stop, operator)
        self.name = 'Simulated Annealing'
        self.Tmax = t_max
        self.Tmin = t_min
        self.alpha = alpha

    def run(self, animation=False):
        """
        Run the Simulated Annealing algorithm to stop when T < Tmin.
        The algorithm generates candidates based on the selected neighbourhood
        operator and will tend to accept less bad moves over time,
        according to the acceptance probability.
        """
        print(f'\nRunning {self.name}. Stopping if no improvement after {self.stop} iterations')
        best_solution = self.generate_init_candidate()
        best_cost = self.evaluate_solution(best_solution)
        T = self.Tmax
        cost_candidates = [best_cost]

        if animation:
            plt.rcParams["figure.figsize"] = (10, 8)
            plt.tight_layout()

        count, its = 0, 0
        while self.Tmin < T and count < self.stop:
            solution_candidate = self.n_op.generate_candidate_solution(best_solution.copy())
            cost_candidate = self.evaluate_solution(solution_candidate)

            acc_prob = self.calculate_acceptance_probability(best_cost, cost_candidate, T)

            if acc_prob > random.random():
                best_solution = solution_candidate.copy()
                best_cost = cost_candidate
                cost_candidates.append(cost_candidate)

                if animation:
                    plt.cla()
                    self.plot_path(best_solution, f'{self.name} using {self.n_op.name}',
                                   f'Iteration: {its} \nCost: {round(best_cost)}')
                    plt.pause(0.05)
                count = 0

            its += 1
            count += 1
            T *= self.alpha  # geometric schedule

        if animation:
            plt.show(block=True)

        return its, cost_candidates, best_solution

    @staticmethod
    def calculate_acceptance_probability(cost_1, cost_2, temperature):
        """
        Acceptance probability = e(-∆E/T), being ∆E=C(S1)-C(S2)
        """
        if cost_1 > cost_2:  # new candidate is already better than current solution
            return 1.0

        return math.exp((cost_1 - cost_2) / temperature)
