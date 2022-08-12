class Chromosome:
    """
    This class represents the chromosome element for GA. It is adapted to TSP so that the encoding/decoding process is
    different from the generic encoding schemes. The constructor needs either the decoded list of cities (tour) or the
    encoded list (ordinal), from which it generates the counterpart.

    Warning: this class is based on the assumption that the starting city of the tour is indexed at 0 and not 1.
    Extra sanity checking could be applied to operate with both types of tour's implementations. But for performance's
    sake, let's assume the tour to follow this format.
    """
    def __init__(self, matrix, tour=None, ordinal=None, elite=False):
        self.fitness = 0
        self.elite_parents = elite

        if tour is not None:
            self.tour = tour
            self.cost = self.evaluate_solution(matrix)
            self.ordinal = self.encode()
        elif ordinal is not None:
            self.ordinal = ordinal
            self.tour = self.decode()
            self.cost = self.evaluate_solution(matrix)

    def evaluate_solution(self, matrix):
        cost = sum(matrix[self.tour[i]][self.tour[i + 1]] for i in range(len(self.tour) - 1))

        # adding the cost from last city in the route to the starting city
        cost += matrix[self.tour[-1]][self.tour[0]]

        return cost

    def encode(self):
        """
        Encode current tour of nodes to ordinal representation
        """
        canonical_tour = list(range(len(self.tour)))
        count = 0
        res = []
        while canonical_tour:
            val = self.tour[count]
            idx = canonical_tour.index(val)
            res.append(idx)
            canonical_tour.pop(idx)
            count += 1

        return res

    def decode(self):
        """
        Decode ordinal representation to the tour of nodes
        """
        canonical_tour = list(range(len(self.ordinal)))
        count = 0
        res = []
        while canonical_tour:
            idx = self.ordinal[count]
            val = canonical_tour[idx]
            res.append(val)
            canonical_tour.pop(idx)
            count += 1

        return res
