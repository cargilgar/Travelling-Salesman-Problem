# Hill Climbing

## Description

Hill climbing is one of the most popular search algorithms since it is easy to implement, uses little memory, and finds a reasonable answer in a large search space.

This algorithm goes through a number of iterations and stops when it reaches a local optimal solution (it might not be the best solution, but it is guaranteed to be the best within its neighbourhood in a relatively quick manner). 
Generally, the termination criterion is, if we do not find a better solution, in x iterations.

Its major disadvantage though, is its tendency to get stuck in local optima, not being able to find the global optimum solution.


## Variants
There are two main variants of the hill climbing algorithm (which can be used in this project): simple and steepest.

### Simple
The simple hill climbing algorithm tries to find a better solution than what it currently has by exploring its neighbourhood space, assigning the candidate solution to the current solution if the candidate solution is better.
However, this algorithm may produce poor results due to moving to a solution that is better than its current solution without exploring the whole neighbourhood space of a candidate solution.

### Steepest (descent)
This variant addresses one of the main issues with the simple hill climbing algorithm, which basically does not explore all its neighbours before selecting the next suboptimal solution. 
Therefore, in the steepest hill climbing algorithm all the immediate neighbours of the current solution are explored and evaluated before committing to a better solution.


As with simple hill climbing, this algorithm still gets stuck in the local optima. Nonetheless, there are a couple of ways to escape from the local optima. 
