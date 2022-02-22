from genetic_algorithm import GeneticAlgorithm


if __name__ == "__main__":
    file = 'TSP_Matrix.csv'

    # Running GA with default parameters
    GA = GeneticAlgorithm(file)
    GA.run()
    #
    # # Running GA with tuned parameters
    # GA = GeneticAlgorithm(file, elitism=0.9, mutation_rate=0.9, crossover_rate=0.6, population_rate=30, stop=50)
    # GA.run()
