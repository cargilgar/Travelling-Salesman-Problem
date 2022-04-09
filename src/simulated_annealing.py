import random
import math
import matplotlib.pyplot as plt

from algorithm import Algorithm


class SimulatedAnnealing(Algorithm):
    """Simulated Annealing Algorithm"""
    def __init__(self, file='', stop=100, operator="inversion", t_max=10, t_min=0.0005, alpha=0.995,
                 cooling_schedule='slow'):
        super().__init__(file, stop, operator)
        self.t_max = t_max
        self.t_min = t_min
        self.current_temp = t_max
        self.alpha = alpha

        self.cooling_schedules_dict = {
            'linear': lambda: self.current_temp - self.alpha,
            'geometric': lambda: self.current_temp * self.alpha,
            'slow': lambda: self.current_temp / (1 + self.alpha * self.current_temp),
            'exp_mult': lambda: self.current_temp * math.pow(self.alpha, self.cycles),
            'linear_mult': lambda: self.current_temp / (1 + self.alpha * self.cycles),
            'quad_mult': lambda: self.current_temp / (1 + self.alpha * math.pow(self.cycles, 2)),
            'log_mult': lambda: self.current_temp / (1 + self.alpha * math.log(1 + self.cycles))
        }

        self.decrease_temperature = self.cooling_schedules_dict.get(cooling_schedule)

    def run(self):
        """
        Run the Simulated Annealing algorithm to stop when T < Tmin.
        The algorithm generates candidates based on the selected neighbourhood
        operator and will tend to accept less bad moves over time,
        according to the acceptance probability.
        """
        print(f'\nRunning {self.__doc__}. Stopping if no improvement after {self.stop} iterations \n')
        best_solution = self.generate_init_candidate()
        best_cost = self.evaluate_solution(best_solution)
        self.current_temp = self.t_max
        cost_candidates = [best_cost]

        plt.rcParams["figure.figsize"] = (10, 8)
        plt.tight_layout()

        count = 0
        while self.t_min < self.current_temp and count < self.stop:
            solution_candidate = self.n_op.generate_candidate_solution(best_solution.copy())
            cost_candidate = self.evaluate_solution(solution_candidate)

            acc_prob = self.calculate_acceptance_probability(best_cost, cost_candidate)

            if acc_prob > random.random():
                best_solution = solution_candidate.copy()
                best_cost = cost_candidate
                cost_candidates.append(cost_candidate)

                plt.cla()
                self.plot_path(best_solution, f'{self.__doc__} using {self.n_op.__doc__}',
                               f'Iteration: {self.cycles} \nCost: {round(best_cost)}')
                plt.pause(0.05)
                count = 0

            self.cycles += 1
            count += 1

            self.current_temp = self.decrease_temperature()

        plt.show(block=True)

        self.plot_convergence(cost_candidates, f'{self.__doc__} minimisation convergence',
                              x_label=f'Total iterations: {self.cycles}', y_label='Cost')

    def calculate_acceptance_probability(self, cost_1, cost_2):
        """
        Acceptance probability = e(-∆E/T), being ∆E=C(S1)-C(S2)
        """
        if cost_1 > cost_2:  # new candidate is already better than current solution
            return 1.0

        return math.exp((cost_1 - cost_2) / self.current_temp)
