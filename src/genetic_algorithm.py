import random
import matplotlib.pyplot as plt

from chromosome import Chromosome
from algorithm import Algorithm

# TODO: consider to dynamically update GA parameters based on learning through control variables


class GeneticAlgorithm(Algorithm):
    def __init__(self, file='', stop=50, neighbourhood_op="rand_swap_adj", elitism=0.8, mutation_rate=1,
                 crossover_rate=1, population_rate=20):
        super().__init__(file, stop, neighbourhood_op)
        self.elitism_rate = elitism
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.population_size = self.nodes * population_rate
        self.create_population(self.population_size)  # Initial population of P chromosomes (generation 0).

    def create_population(self, size):
        for _ in range(size):
            solution = self.generate_init_candidate(self.nodes)
            chromosome = Chromosome(self.matrix.matrix, tour=solution)
            self.population.append(chromosome)

        self.fitness_function()

    def fitness_function(self):
        """
        Since TSP is a minimisation problem, high fitness values are to be associated with short-length paths. This
        fitness function makes the conversion. It also sorts population by descending order of fitness scores.
        """
        max_cost = max([i.cost for i in self.population])

        for chromosome in self.population:
            chromosome.fitness = max_cost - chromosome.cost

        # Population sorted in descending order. The elite chromosomes (better fitness scores) will be located first
        self.population.sort(key=lambda i: i.fitness, reverse=True)

    def remove_duplicates(self):
        """
        Remove chromosomes with the same tour that have been created along the reproduction process.
        """
        unique_population, temp_list = [], []

        for chromosome in self.population:
            if chromosome.tour not in temp_list:
                temp_list.append(chromosome.tour)
                unique_population.append(chromosome)

        self.population = unique_population.copy()

    def fill_missing_population(self):
        if (diff := (self.population_size - len(self.population))) > 0:
            self.create_population(diff)

    def selection(self):
        """
        Roulette Wheel selection:
        1. Sum up the fitness values of all chromosomes in the population.
        2. Generate a random number between 0 and the sum of the fitness values.
        3. Select the first chromosome whose fitness value added to the sum of the fitness
           values of the previous chromosomes is greater than or equal to the random number.

        Warning: this approach may lead to premature convergence, as super-chromosomes with high fitness values will
        quickly dominate the population.
        """
        # Selecting elite chromosomes
        elite = int(self.population_size * self.elitism_rate)
        selection = self.population[:elite]

        # Step 1
        total_fitness = sum([i.fitness for i in self.population])

        while len(selection) < self.population_size:
            # Step 2
            rand = random.randint(0, int(total_fitness))
            i = random.choice(self.population)

            # Step 3
            if i.fitness >= rand:
                selection.append(i)

        self.population = selection.copy()
        self.fitness_function()

    def crossover(self):
        """
        One-point crossover to produce two offspring. It selects at random a pair of parents for mating, ensuring that
        a number of parents based on the crossover rate are selected and mated.
        """
        # Get a random number of chromosomes that are selected to be parents
        occurrences = random.sample(range(0, self.population_size), int(self.population_size * self.crossover_rate))

        # Get elites of current population, their offspring are expected not to receive mutation.
        elites = self.population[:int(self.population_size * self.elitism_rate)]

        parents = [self.population[i] for i in occurrences]
        parents_size = len(parents)

        # Removing selected parents for mating from population so that their offspring replace their position.
        for occurrence in sorted(occurrences, reverse=True):
            self.population.pop(occurrence)

        offspring = []

        while len(offspring) < parents_size and len(parents) > 0:
            # Select two parents randomly for mating
            parent_1_selector = random.randint(0, len(parents) - 1)
            parent_1 = parents[parent_1_selector]
            parents.pop(parent_1_selector)

            parent_2_selector = random.randint(0, len(parents) - 1)
            parent_2 = parents[parent_2_selector]
            parents.pop(parent_2_selector)

            # One-point divider
            i = random.randint(0, self.nodes)

            # Crossover
            crossover = parent_1.ordinal[:i] + parent_2.ordinal[i:]
            child_1 = Chromosome(self.matrix.matrix, ordinal=crossover)
            crossover = parent_1.ordinal[:i] + parent_2.ordinal[i:]
            child_2 = Chromosome(self.matrix.matrix, ordinal=crossover)

            # Mark offspring which parents (at least one) are elite
            if parent_1 in elites or parent_2 in elites:
                child_1.elite_parents = True
                child_2.elite_parents = True

            offspring.append(child_1)
            offspring.append(child_2)

        # Add new offspring to the population alongside the chromosomes not selected for reproduction (older generation)
        for chromosome in offspring:
            self.population.append(chromosome)

        assert (new_size := len(self.population)) == (initial_size := self.population_size), \
            f'Error: size of new population: {new_size} is different from initial size: {initial_size}'

    def mutation(self):
        """
        Introducing diversity by introducing perturbations in a number of randomly selected offspring (determined by the
        mutation rate). Insert the resulting offspring in the new population.
        """
        occurrences = random.sample(range(0, self.population_size), int(self.population_size * self.mutation_rate))

        for occurrence in occurrences:
            chromosome = self.population[occurrence]
            if not chromosome.elite_parents:
                new_tour = self.n_op.generate_candidate_solution(chromosome.tour.copy())
                mutated = Chromosome(self.matrix.matrix, tour=new_tour)
                self.population[occurrence] = mutated

        # End mutation by recalculating the fitness scores and sorting the population
        self.fitness_function()

    def run(self, animation=False):
        print(f'\nRunning Genetic Algorithm. Stopping if no improvement after {self.stop} iterations')
        best_chromosome = self.population[0]
        best_costs = []

        if animation:
            plt.rcParams["figure.figsize"] = (10, 8)
            plt.tight_layout()

        count, its = 0, 0
        while count < self.stop:
            self.selection()
            self.crossover()
            self.mutation()

            if self.population[0].cost < best_chromosome.cost:
                best_chromosome = self.population[0]
                print(f'Better chromosome found. Cost: {round(best_chromosome.cost)}')
                best_costs.append(best_chromosome.cost)

                if animation:
                    plt.cla()
                    self.plot_path(best_chromosome.tour, f'Genetic Algorithm using {self.n_op.name}',
                                   f'Iteration: {its} \nCost: {round(best_chromosome.cost)}')
                    plt.pause(0.05)

                count = 0
            else:
                count += 1

            its += 1

            # Restructure population if necessary for next reproduction stage
            self.remove_duplicates()
            self.fill_missing_population()

        if animation:
            plt.show()

        # return best_chromosome
        return its, best_costs, best_chromosome.tour
