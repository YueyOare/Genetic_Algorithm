import random

import pandas as pd
from scipy import optimize

counter = 0

def fitness_function(x):
    global counter
    counter += 1
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2


def generate_population(size, low, high):
    population = []
    for i in range(size):
        individual = {
            'genes': [(random.uniform(low, high), random.uniform(low, high))],
            'fitness': None
        }
        population.append(individual)
    return population


def evaluate_population(population):
    for individual in population:
        x = individual['genes'][0]
        individual['fitness'] = fitness_function(x)


def select_best_individuals(population, k):
    population.sort(key=lambda x: x['fitness'])
    return population[:k]


def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        child_genes = []
        for i in range(len(parent1['genes'])):
            if random.random() < 0.5:
                child_genes.append(parent1['genes'][i])
            else:
                child_genes.append(parent2['genes'][i])
        child = {
            'genes': child_genes,
            'fitness': None
        }
        return child
    else:
        return None


def mutate_genes(individual, mutation_rate, low, high):
    for i in range(len(individual['genes'])):
        if random.random() < mutation_rate:
            individual['genes'][i] = (random.uniform(low, high), random.uniform(low, high))


def create_new_population(old_population, elitism_k,
                          crossover_rate, mutation_rate, low, high):
    new_population = []
    best_individuals = select_best_individuals(old_population, elitism_k)
    for i in range(len(old_population) - elitism_k):
        parent1 = random.choice(best_individuals)
        parent2 = random.choice(best_individuals)
        child = crossover(parent1, parent2, crossover_rate)
        if child is None:
            child = parent1
        mutate_genes(child, mutation_rate, low, high)
        new_population.append(child)
    new_population.extend(best_individuals)
    return new_population


def create_table(population):
    gen = {'№ хромосомы': [], 'Значение функции': [], 'Ген 1 (х1)': [], 'Ген 2 (х2)': []}
    for i in range(len(population)):
        gen['№ хромосомы'].append(i+1)
        gen['Значение функции'].append(population[i]['fitness'])
        gen['Ген 1 (х1)'].append(population[i]['genes'][0][0])
        gen['Ген 2 (х2)'].append(population[i]['genes'][0][1])
    return pd.DataFrame(gen)


def genetic_algorithm(pop_size=50, num_generations=10, elitism_k=2, crossover_rate=0.8, mutation_rate=0.1, low=-50, high=50):
    global counter
    counter = 0
    population = generate_population(pop_size, low, high)
    evaluate_population(population)
    output = [create_table(population)]
    for i in range(num_generations):
        population = create_new_population(population, elitism_k, crossover_rate, mutation_rate, low, high)
        evaluate_population(population)
        output.append(create_table(population))
    best_individual = min(population, key=lambda x: x['fitness'])
    return best_individual['genes'][0], best_individual['fitness'], output, counter


# x, y, output = genetic_algorithm(pop_size=50, num_generations=10, elitism_k=2, crossover_rate=0.8, mutation_rate=0.1, low=-50, high=50)
# print('Точка минимума:', x, '\nМинимум функции:', y)
# for generation in output:
#     print(generation)