import matplotlib.pyplot as plt


class Chromosome:
    """
    This class represents the chromosome element for GA. It is adapted to TSP so that the encoding/decoding process is
    different from the generic encoding schemes. The constructor needs either the decoded list of cities (tour) or the
    encoded list (ordinal), from which it generates the counterpart.

    Warning: this class is based on the assumption that the starting city of the tour is indexed at 0 and not 1.
    Extra sanity checking could be applied to operate with both types of tour's implementations. But for performance's
    sake, let's assume the tour to follow this format.
    """
    def __init__(self, matrix, tour=None, ordinal=None):
        self.fitness = 0

        if tour is not None:
            self.tour = tour
            self.cost = self.evaluate_solution(matrix)
            self.ordinal = self.encode()
        elif ordinal is not None:
            self.ordinal = ordinal
            self.tour = self.decode()
            self.cost = self.evaluate_solution(matrix)

    def evaluate_solution(self, matrix):
        cost = 0
        for i in range(len(self.tour) - 1):
            cost += matrix[self.tour[i]][self.tour[i + 1]]

        # adding the cost from last city in the route to the starting city
        cost += matrix[self.tour[-1]][self.tour[0]]

        return cost

    def encode(self):
        """
        Encode current tour of nodes to ordinal representation
        """
        canonical_tour = list(range(0, len(self.tour)))
        count = 0
        res = []
        while len(canonical_tour) > 0:
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
        canonical_tour = list(range(0, len(self.ordinal)))
        count = 0
        res = []
        while len(canonical_tour) > 0:
            idx = self.ordinal[count]
            val = canonical_tour[idx]
            res.append(val)
            canonical_tour.pop(idx)
            count += 1

        return res

    def plot(self, coord, title):
        """
        Plot the tour of the chromosome.
        """
        x_coord, y_coord = [], []

        for item in coord:
            x_coord.append(item[0])
            y_coord.append(item[1])

        path_x, path_y = [], []
        for val in self.tour:
            path_x.append(x_coord[val])
            path_y.append(y_coord[val])

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(path_x, path_y, color='black')

        plt.suptitle(title, fontsize=16)

        # adding the last city to come back to the starting point
        path_x.append(path_x[0])
        path_y.append(path_y[0])

        plt.plot(path_x, path_y, color='green')

        plt.show()
