# Simulated Annealing

## Description
Simulated annealing (also known as **Monte Carlo annealing**, **probabilistic hill climbing** or **stochastic relaxation**) is inspired from the process of annealing in metals. 
Annealing involves heating and then steadily cooling the metal material to change its physical properties due to the changes in its internal structure.

In the simulated annealing method, a high temperature variable is used to simulate this annealing process. The temperature variable is set at 'high' and allowed to slowly cool down as the algorithm goes through its iterations. At the beginning, a random neighbouring solution is generated and evaluated. 

At a high temperature, the algorithm is allowed to accept worse solutions than its current solution. With the drop in temperature, the probability of accepting worse solutions is also reduced. Therefore, allowing the algorithm to gradually focus on an area of the search space in which hopefully, a close to optimum solution can be found.

## Criterion evaluation
The algorithm generates new solutions by exploring the neighbourhood of the current solution. If the new solution is better than the current solution, then the new solution is accepted as a current solution straight away. 

However, if the new solution is not better than the current solution, then the new solution can still be accepted based on the change in the fitness values of the solutions (*∆E*) and the current temperature.

## Bad move acceptance
If the neighbour's solution is better than our current solution, then we accept it unconditionally. If, however, the neighbour solution is not better we need to consider a couple of factors.

Firstly, how much worse the neighbour solution is; and secondly, how high the current temperature of our system is.

The bad moves are accepted based on the probability that follows the [Boltzmann distribution](https://en.wikipedia.org/wiki/Boltzmann_distribution), and which is derived from the interaction between the current temperature and the *∆E* (change of energy), 
which is a function of change in cost divided by the current temperature:

<p align="center">
  <img src="http://www.sciweavers.org/tex2img.php?eq=P%5Cbig%28%E2%88%86E%2CT%5Cbig%29%20%3D%20exp%28%5Cfrac%7B%20%5Cpartial%20E%7D%7BT%7D%29%20%3E%20R&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" />
</p>


The resulting probability can be compared to a uniform random number from 0 to 1. Insofar as *T* decreases, so will *P*, and it will be more and more difficult to get a *P* higher than *R*. 
In other words, when *T* gets close to 0, only good moves will be accepted.

## Cooling schedule or cooling down factor (alpha)
The cooling schedule allows adequate iterations at each temperature before decreasing the temperature. The cooling schedule may be of different forms. One very common is the geometric: 

<p align="center">
  <img src="http://www.sciweavers.org/tex2img.php?eq=T%20%3D%20T%20%2A%20alpha&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" />
</p>

However, other cooling schedules can be explored such as linear, logarithmic (it can be slow) or adaptive, among others (see literature).

## Advantages of SA

This gradual *cooling* process is what makes the simulated annealing algorithm remarkably effective at finding a close to optimum solution when dealing with large problems which contain numerous local optimal (escaping from the local optima).

Moreover, SA is a memory-less algorithm in the sense that the algorithm does not use any information gathered during the search.
Note: the stochastic hill-climber algorithm is the same as simulated annealing but keeping T constant during the run.

## Disadvantages of SA
SA requires to set the minimum and maximum temperature at an adequate level. If the initial temperature is **too low**, SA algorithm will behave similarly to hill climbing algorithm. 

At the same time, if the starting temperature is kept **too high**, then the algorithm will accept too many bad solutions and will take a long time to get to a stabilisation phase, being the risk of the algorithm behaving like a random walk algorithm (random search). In fact, for huge values of initial T, the probability of acceptance becomes 0.5 (random search).

The same applies to the cooling schedule. **Too high** alpha will not allow enough exploration and will converge to a local optimum solution too fast, **too low** alpha will take too much time to cool down.
