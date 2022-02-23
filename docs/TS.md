# Tabu Search (TS)

## Description
The main idea of tabu search is to keep a list of moves to avoid exploring previously explored paths. 

This tabu list is also called short-term memory. It is not possible to store all the moves, so a finite list of tabu moves is stored.

Tabu lists can be considered very restrictive; therefore, under some special circumstances, tabu moves are allowed. Those conditions are called **aspiration criteria**. 

The common aspiration criterion is when the candidate solution is better than the best solution obtained so far during the search. 
Similar to [SA](SA.md#Simulated-Annealing), Tabu Search accepts bad moves by always accepting the best neighbourhood move even if the solution is worse than the current solution's best solution (given that the move is not tabu).

Unlike SA, this algorithm makes use of memory, with the trade-off of being able to get a solution in a relative quickly manner. Thus, this algorithm may not be suitable if it is to be used on a device with memory constraints.

## Tabu tenure
This is an important concept in tabu search. It deals with the duration of time any element of tabu search will remain forbidden.

Tabu tenure is a very efficient algorithm; however, in order to obtain the best results, the concepts of medium-term memory and long-term memory are also incorporated in this algorithm.

## Medium-term memory
This is also called **intensification** (or exploitation). The idea here is to identify the most promising regions (features) in the best solutions and intensify the search around those regions. 

A common approach is to start with the best solution and fix the most promising features derived through the recency memory.

## Long-term memory
Short- and medium-term memory concepts are used to exploit the solutions around the feasible regions. The component of long-term memory has been incorporated in the tabu search to facilitate the exploration of the search space. 

The frequency memory is used in long-term memory. In the context of TSP, frequency memory will be ordered by pairs of edges swapped (or reconnected) in previous solutions.

