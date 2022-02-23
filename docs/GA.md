# Genetic Algorithm

## Description
A genetic algorithm is a P-metaheuristic evolutionary algorithm (EA) that mimics the concept of the survival of the fittest, being the individuals with the most promising genetic properties, being able to thrive and survive among other individuals.

The advantages of GA's are that they can simulate many points in any given parameter space. At each new generation, the algorithm explores different areas of the parameter space guiding the search to the fittest regions or those with improved performance. This then increases the likelihood of finding the optimal global solution.


## Parameter tuning
The performance of any GA is greatly affected by the setting of some parameters known as **parameter tuning**.

The class `GeneticAlgorithm` has been set with a series of predefined parameters which are the result of having carried out different pilot runs on different small-scale search spaces seeking to obtain optimal parameters that would generally perform well on any given search space.

However, these parameters are by no means set in stone, and it is recommended to modify them accordingly to the specific problem. Nonetheless, they are good starting point before tuning.

**GA operators**
* Selection operator: it selects chromosomes to be parents for reproduction (crossover) prevailing chromosomes with high fitness scores based on probability. The higher the fitness means the higher chance of 
being selected. Also, elite chromosomes are selected automatically in this step.  
  - Only one available (for now): Roulette Wheel Selection.
* Crossover operator: it allows us to escape local optima by exploring other neighbourhoods with potential better solutions. 
  - Only one available (for now): One-point Crossover<sup>[1](#footnote)</sup>
* Mutation operator: it helps explore the new neighbourhood searches discovered after crossover (it introduces perturbations in the offspring generated). 
  - For TSP, these are the standard neighbourhood operators. There are some available under `utils/n_ops`.

**Parameters to be tuned** [1]
* Elitism rate (parent rate): it determines the percentage of parents with the best fitness score to be selected at first before starting the selection process. By default: 0.8. To choose from: 0-1
* Crossover rate: it determines the number of times a crossover occurs for chromosomes in one generation (i.e., the chance that a pair of parents mate). By default: 1. To choose from: 0-1
* Mutation rate: it determines how many offspring should be mutated in one generation. By default: 1. To choose from: 0-1
* Population rate: it defines the total population size which is proportionally related to the number of nodes (cities) given by the search space. By default: 20 (for good results, it is recommended not to choose a population rate smaller than 10).

*****

<a name="footnote">1</a>: For the TSP, classical crossover operators such as one-point, two-point, and uniform crossovers are not suitable with the normal path representation.
With this representation, crossover can be responsible for producing unfeasible solutions.

For example: 1-point crossover for 50% crossover:

Parent 1: **A F D C** H B G E

Parent 2: C B A D **E H G F**

Offspring: A F D C E H G F

Here, the resulting offspring has the node **F** duplicated, and does not have the node **B** at all, which is an unfeasible solution for TSP.

There are some approaches present in the literature to deal with such constraints, such as removing unfeasible solutions, repairing them, using specialised operators (e.g., PMX or OX crossover) or transforming the search space.

The latter is the approach taken here. The reason for this is to simply follow the spirit of the standard crossover operators of GA by modifying the standard chromosomes, instead of completely manipulating the whole operator.

This approach is as follows: the search space is transformed to an ordinal representation (encoding) [2], [3]. This in turn, can be easily transformed back to the tour of nodes (decoding). This encoding/decoding process is carried out within the class `Chromosome` in `chromosome.py`.

*****

## References
[1] M. Mosayebi and M. Sodhi, “Tuning genetic algorithm parameters using design of experiments,” in Genetic and Evolutionary Computation Conference, Cancun, Mexico, 2020.

[2] J.-Y. Potvin, “Genetic algorithms for the travelling salesman problem,” Annals of Operations Research, vol. 63, pp. 337-370, 1996.

[3] A. Mohebifar, “New binary representation in genetic algorithms for solving tsp by mapping permutations to a list of ordered numbers”.
