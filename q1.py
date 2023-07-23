import numpy as np
import torch


class AntColonyOptimizer:
    def __init__(self, filename, num_ants=100, num_iterations=100, decay=0.1, alpha=1, beta=1, Q=1):
        self.filename = filename
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.Q = Q
        self.distances = torch.tensor(self.load_adjacency_matrix(filename), dtype=torch.float)
        self.pheromones = torch.ones((8, 8))

    @staticmethod
    def load_adjacency_matrix(filename):
        return np.loadtxt(filename, delimiter=',')

    def solve(self):
        for i in range(self.num_iterations):
            # Initialize ants' routes
            routes = torch.zeros((self.num_ants, 8)).long()

            # Start each ant at a different city
            routes[:, 0] = torch.arange(self.num_ants) % 8

            for j in range(1, 8):
                for k in range(self.num_ants):
                    current_city = routes[k, j-1]

                    # Probabilities for moving to each city
                    probs = (self.pheromones[current_city]**self.alpha / (self.distances[current_city] + 1e-10)**self.beta)

                    # Set probabilities to 0 for already visited cities
                    probs[routes[k, :j]] = 0

                    # Normalize probabilities
                    probs = probs / probs.sum()

                    # Choose next city
                    routes[k, j] = torch.multinomial(probs, 1).item()

            # Compute cost
            cost = torch.zeros(self.num_ants)
            for j in range(8):
                from_city = routes[:, j-1]
                to_city = routes[:, j]
                cost += self.distances[from_city, to_city]
            cost += self.distances[routes[:, -1], routes[:, 0]]  # return to starting city

            # Update pheromones
            self.pheromones *= (1 - self.decay)
            for j in range(8):
                from_city = routes[:, j-1]
                to_city = routes[:, j]
                for k in range(self.num_ants):
                    self.pheromones[from_city[k], to_city[k]] += self.Q / cost[k]

        best_route = routes[cost.argmin()]
        best_cost = cost.min()

        return best_route, best_cost


if __name__ == "__main__":
    aco = AntColonyOptimizer('adjacency.txt')
    route, cost = aco.solve()

    print('Best route: ', route)
    print('Best cost: ', cost)
