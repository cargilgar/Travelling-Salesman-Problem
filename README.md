# Travelling Salesman Problem Example

The Travelling Salesman Problem (TSP) is an **NP-hard** (non-deterministic polynomial) problem in combinatorial optimisation.

Its growing complexity in real-world applications makes it unfeasible to compute an exact solution in a reasonable amount of time (even for super computers).

For this reason, three approximate algorithms are presented in this repository to offer approximate and yet robust solutions to this problem in a reasonable amount of computational time nad resources.

## Table of contents

- [Problem description](#Problem-description)
- [Instructions](#Instructions)
- [References](#References)
- [Algorithms](#Algorithms)
- [Neighbourhood operators](#Neighbourhood-operators)


## Problem description

Given a number of cities *n* and the distance matrix between each pair of cities *d*, the goal is to find the shortest route that visits each city just once and returns to the starting city.

In this example, we attempt to solve this problem by employing different pathfinding algorithms that rely on heuristic search in order to find an optimum path.

In order to achieve this, we need to take care of the following steps:
1. **Algorithm selection**: To be chosen from here [Algorithms](#Algorithms).
2. **Neighbourhood operator**: To be chosen from here [Neighbourhood operators](#Neighbourhood-operators).
3. **Initial Solution**: this can be either random (by default) or greedy approach.
4. **Solution evaluation**: for this problem, this is simply adding the cost of travelling through the cities.
5. **Stopping criteria**: No improvement after some iterations or conditions. Note that each algorithm has its own criteria for stopping.

## Instructions:
```bash
pip install requirements.txt

cd src/

python main.py
```
You can use any of the [algorithms](#Algorithms) and modify their parameters to explore different behaviours. You can activate an animation to see how the algorithm progresses during the heuristic search process by setting: 

```py
run(animation=True)
```

Note: a version of **Python 3.8** or greater is needed in order to run this program. 

## Algorithms
Algorithms for this problem:
* [Simulated Annealing](#Simulated-Annealing) (SA)
* [Tabu Search](#Tabu-Search) (TS)
* [Genetic Algorithm](#Genetic-Algorithm) (GA)

## Neighbourhood operators
Similarly, the following neighbourhood operators are available to choose from:
* Random exchange (`key='ran_swap'`)
* Random exchange Adjacent cities (`key='ran_swap_adj'`)
* Inversion (`key='inversion'`)
* 2-opt (`key='two_opt'`)


# Simulated Annealing
Simulated annealing is an S-metaheuristic algorithm that...


# Tabu Search
Tabu Search is an S-metaheuristic algorithm that...


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
