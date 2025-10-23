import numpy as np
import pandas as pd
import random

class GeneticLinearRegression:
    def __init__(self, pop_size=50, n_generations=100, crossover_rate=0.8, mutation_rate=0.1):
        self.pop_size = pop_size
        self.n_generations = n_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.best_weights = None
        self.best_fit = -1

    # ====== Evaluation ======
    def evaluate_individual(self, X, weights=None):
        if weights is None:
            weights = self.best_weights
        if weights is None:
            raise ValueError("Model is not trained or loaded weights!")
        return weights[0] + np.dot(X, weights[1:])

    # ====== Population Initialization ======
    def _init_population(self, n_features):
        return [np.random.uniform(-10, 10, n_features + 1) for _ in range(self.pop_size)]

    # ====== Fitness ======
    def _fitness(self, X, y, weights):
        y_pred = self.evaluate_individual(X, weights)
        mse = np.mean((y - y_pred) ** 2)
        return 1 / (mse + 1e-6)

    # ====== Selection ======
    def _selection(self, population, fitnesses):
        total_fit = sum(fitnesses)
        probs = [f / total_fit for f in fitnesses]
        return population[np.random.choice(len(population), p=probs)]

    # ====== Crossover ======
    def _crossover(self, p1, p2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(p1) - 1)
            c1 = np.concatenate([p1[:point], p2[point:]])
            c2 = np.concatenate([p2[:point], p1[point:]])
            return c1, c2
        else:
            return p1.copy(), p2.copy()

    # ====== Mutation ======
    def _mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] += np.random.normal(0, 1)
        return individual

    # ====== Train GA ======
    def fit(self, X, y):
        n_features = X.shape[1]
        population = self._init_population(n_features)

        for gen in range(self.n_generations):
            fitnesses = [self._fitness(X, y, ind) for ind in population]
            
            gen_best_idx = np.argmax(fitnesses)
            gen_best_fit = fitnesses[gen_best_idx]
            if gen_best_fit > self.best_fit:
                self.best_fit = gen_best_fit
                self.best_weights = population[gen_best_idx].copy()  # ← Quan trọng: .copy()
            
            new_population = []
            for _ in range(self.pop_size // 2):
                p1 = self._selection(population, fitnesses)
                p2 = self._selection(population, fitnesses)
                c1, c2 = self._crossover(p1, p2)
                c1 = self._mutate(c1)
                c2 = self._mutate(c2)
                new_population.extend([c1, c2])

            population = new_population

            if gen % 10 == 0:
                mse = 1 / (self.best_fit + 1e-6) - 1e-6
                print(f"Generation {gen:3d} | Best MSE: {mse:.6f} | Fitness: {self.best_fit:.6f}")

        print("\n✅ Training complete.")
        print("Best weights:", self.best_weights)

    def save_model(self, path="src/weights/model_weights.npy"):
        if self.best_weights is not None:
            np.save(path, self.best_weights)
            print(f"💾 Model saved to {path}")
        else:
            print("⚠️ Warning: No weights to save. Model may not have been trained.")

    def load_model(self, path="src/weights/model_weights.npy"):
        self.best_weights = np.load(path)
        print(f"📂 Model loaded from {path}")

    def predict(self, X):
        if self.best_weights is None:
            raise ValueError("Model is not trained or loaded weights!")
        return self.evaluate_individual(X, self.best_weights)
    
    # ====== Classmethod for inference only ======
    @classmethod
    def from_weights(cls, weights_path):
        model = cls(pop_size=1, n_generations=1)
        model.load_model(weights_path)
        return model