import matplotlib.pyplot as plt
import random
import math

from algorithm import Algorithm


class SimulatedAnnealing(Algorithm):
    def __init__(self, file='', stop=100, operator="inversion", t_max=10, t_min=0.0005, alpha=0.995,
                 cooling_schedule='slow'):
        super().__init__(file, stop, operator)
        self.name = 'Simulated Annealing'
        self.Tmax = t_max
        self.Tmin = t_min
        self.T = t_max
        self.alpha = alpha
        self.schedule = cooling_schedule

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
        self.T = self.Tmax
        cost_candidates = [best_cost]

        if animation:
            plt.rcParams["figure.figsize"] = (10, 8)
            plt.tight_layout()

        count, self.cycles = 0, 0
        while self.Tmin < self.T and count < self.stop:
            solution_candidate = self.n_op.generate_candidate_solution(best_solution.copy())
            cost_candidate = self.evaluate_solution(solution_candidate)

            acc_prob = self.calculate_acceptance_probability(best_cost, cost_candidate)

            if acc_prob > random.random():
                best_solution = solution_candidate.copy()
                best_cost = cost_candidate
                cost_candidates.append(cost_candidate)

                if animation:
                    plt.cla()
                    self.plot_path(best_solution, f'{self.name} using {self.n_op.name}',
                                   f'Iteration: {self.cycles} \nCost: {round(best_cost)}')
                    plt.pause(0.05)
                count = 0

            self.cycles += 1
            count += 1

            self.decrease_temperature()

        if animation:
            plt.show(block=True)

        return cost_candidates, best_solution

    def calculate_acceptance_probability(self, cost_1, cost_2):
        """
        Acceptance probability = e(-∆E/T), being ∆E=C(S1)-C(S2)
        """
        if cost_1 > cost_2:  # new candidate is already better than current solution
            return 1.0

        return math.exp((cost_1 - cost_2) / self.T)

    def decrease_temperature(self):
        if self.schedule == 'linear':
            self.T -= self.alpha
        elif self.schedule == 'geometric':
            self.T *= self.alpha
        elif self.schedule == 'slow':
            self.T = self.T / (1 + self.alpha * self.T)
        elif self.schedule == 'exp_mult':
            self.T *= math.pow(self.alpha, self.cycles)
        elif self.schedule == 'linear_mult':
            self.T = self.T / (1 + self.alpha * self.cycles)
        elif self.schedule == 'quad_mult':
            self.T = self.T / (1 + self.alpha * math.pow(self.cycles, 2))
        elif self.schedule == 'log_mult':
            self.T = self.T / (1 + self.alpha * math.log(1 + self.cycles))
