import matplotlib.pyplot as plt
import random
import time
import os

ALLELE_POOL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !.,?"
TARGET_SOLUTION = "Hello World!"



class GeneticAlgorithm():

    class Individual():
        def __init__(self, chromosome):
            """
            :param chromosome: A string the same size as TARGET_SOLUTION
            """
            self.chromosome = chromosome
            self.fitness = self.get_fitness()
            
        def get_fitness(self):
            """
            :return: A numerical value being the fitness of the individual.
            """
            fitness = 0
            chromosome = self.get_chromosome()
            taille = len(chromosome)

            for i in range(taille):
                if chromosome[i] == TARGET_SOLUTION[i]:
                    fitness += 1

            return fitness
        
        def get_chromosome(self):
            """
            :return: A string, the chromosome of the individual. 
            """
            return self.chromosome
        
    def __init__(self, pop_size = 500, pm = 0.01, elitism = 0.05):
        """
        :param pop_size: An integer defining the size of the population
        :param pm: A float defining the mutation rate
        :param elitism: A float definism the elitism rate
        """
        self.pop_size = pop_size
        self.allele_pool = ALLELE_POOL
        self.mutation_rate = pm
        self.elitism = elitism

    def generate_generation_zero(self):
        """
        :return: A list of size self.pop_size
                 containing randomly generated instances
                 of the class Individual
        """
        population = list()
        for i in range(self.pop_size):
            chromosome = ""
            for j in range(len(TARGET_SOLUTION)):
                chromosome += "".join(random.choices(self.allele_pool))
            population.append(self.Individual(chromosome))
        return population


    def mutation(self, individual):
        """
        :param chromosome: An instance of the class Individual
                           whose chromosome is to mutate
        :return:  An instance of the class Individual
                  whose chromosome has been mutated
        """
        prob_mutation = self.mutation_rate
        mutated_chromosome = individual
        for i in range(len(mutated_chromosome)):
            if random.uniform(0, 1) < prob_mutation:
                mutated_chromosome = mutated_chromosome[:i] + "".join(random.choices(self.allele_pool)) + mutated_chromosome[i+1:]
        return self.Individual(mutated_chromosome)
    
    def selection(self, population, mating_pool_size_ratio=0.5):
        """
        :param population : A list of instances of the class Individuals
        :return: The mating pool constructed from
                the 50% fittest individuals in the population
        """
        mating_pool = list()
        sortedPopulation = sorted(population, key=lambda individual: individual.get_fitness(), reverse=True)
        for i in range(int(self.pop_size * mating_pool_size_ratio)):
            mating_pool.append(sortedPopulation[i])
        return mating_pool

        
    def create_offspring(self, parent1, parent2, crossover_type="single"):
        """
        Crée deux descendants à partir de deux parents en utilisant
        le crossover spécifié.
    
        :param parent1: Instance de la classe Individual.
        :param parent2: Instance de la classe Individual.
        :param crossover_type: Type de crossover ("single" ou "double").
        :return: Deux chromosomes/strings créés par le crossover.
        """
        chromosome1, chromosome2 = parent1.get_chromosome(), parent2.get_chromosome()

        if crossover_type == "single":
            # Single-point crossover
            indexCrossover = random.randint(0, len(chromosome1))
            offspring1 = chromosome1[:indexCrossover] + chromosome2[indexCrossover:]
            offspring2 = chromosome2[:indexCrossover] + chromosome1[indexCrossover:]

        elif crossover_type == "double":
            # Double-point crossover
            point1 = random.randint(0, len(chromosome1) - 2)
            point2 = random.randint(point1 + 1, len(chromosome1))
            offspring1 = (
                chromosome1[:point1] + chromosome2[point1:point2] + chromosome1[point2:]
            )
            offspring2 = (
                chromosome2[:point1] + chromosome1[point1:point2] + chromosome2[point2:]
            )
         
        return (offspring1, offspring2)
    
    def run_genetic_algorithm(self, seed, 
                              tol = 0.0,
                              display = True, mating_pool_size_ratio=0.5, crossover_type="single"):
        """
        :param seed: An integer to set the random seed
        :param tol: A tolerance on the fitness function
        :param display: A boolean. If True, the fitness 
                        of the best performing individual
                        is displayed at the end of each 
                        generation
        """

        random.seed(seed)
        generation = 0

        # 1. Random generation of the initial population
        population = self.generate_generation_zero()

        # --- Modify the convergence criteria ---
        while(population[0].get_fitness() < tol): 
        
            if display:
                print("Generation {} - {} : {}\n".format(
                    generation,
                    int(len(TARGET_SOLUTION) - population[0].get_fitness()),
                    population[0].get_chromosome())),

            # 2. Creation of the mating pool
            mating_pool = self.selection(population, mating_pool_size_ratio)

            
            # 3. Apply the elistist strategy
            n_elites = int(self.elitism * self.pop_size)
            new_population = population[:n_elites]

            # 4. Continuing the breeding process until
            # the population is entirely renewed
            while len(new_population) < self.pop_size:
                    
                    # 4.1 Select the parent in the mating pool 
                    parent1 = random.choice(mating_pool)
                    parent2 = random.choice(mating_pool)

                    # 4.2 Make them reproduce 
                    offspring1, offspring2 = self.create_offspring(parent1, parent2, crossover_type)

                    # 4.3 Mutate the offsprings
                    offspring1 = self.mutation(offspring1)
                    offspring2 = self.mutation(offspring2)

                    # 4.4 Append the new solutions to the new population
                    new_population += [offspring1, offspring2] 
            

            # The (sorted) new population replace the previous one. 
            population = sorted(new_population, key= lambda individual : individual.get_fitness(), reverse=True)
            generation += 1

        if display: 
            print("Generation {} : {}, fitness = {} \n".format(
                    generation,
                    population[0].get_chromosome(), 
                    population[0].get_fitness()))

        return generation, population[0].fitness, population[0].get_chromosome()


os.system('mkdir -p plots')

# Liste des seeds
num_seeds = 1
seeds = list(range(num_seeds))

# Liste des tailles de population à tester
population_sizes = [10, 20, 30, 40, 50, 60, 70 , 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
generations_needed = []
execution_times = []

# Tester chaque taille de population
for pop_size in population_sizes:
    generations_accumulated = []
    execution_times_accumulated = []

    # Exécuter pour chaque seed
    for seed in seeds:
        ga = GeneticAlgorithm(pop_size=pop_size)

        # Mesurer le temps d'exécution
        start_time = time.time()
        generations, fitness, chromosome = ga.run_genetic_algorithm(
            seed=seed, 
            tol=len(TARGET_SOLUTION), 
            display=False  # Désactiver l'affichage pour les tests multiples
        )
        end_time = time.time()
        
        # Accumuler les résultats
        generations_accumulated.append(generations)
        execution_times_accumulated.append(end_time - start_time)
    
    # Moyenne sur les seeds
    avg_generations = sum(generations_accumulated) / len(seeds)
    avg_execution_time = sum(execution_times_accumulated) / len(seeds)
    
    generations_needed.append(avg_generations)
    execution_times.append(avg_execution_time)

# Tracer le graphique
fig, ax1 = plt.subplots(figsize=(10, 6))

# Premier axe : nombre de générations
color1 = 'tab:blue'
ax1.set_xlabel("Taille de la population")
ax1.set_ylabel("Nombre de générations nécessaires", color=color1)
ax1.plot(population_sizes, generations_needed, marker='o', linestyle='-', color=color1, label="Nombre de générations")
ax1.tick_params(axis='y', labelcolor=color1)

# Second axe : temps d'exécution
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel("Temps d'exécution (s)", color=color2)
ax2.plot(population_sizes, execution_times, marker='o', linestyle='--', color=color2, label="Temps d'exécution")
ax2.tick_params(axis='y', labelcolor=color2)

# Titre et légendes
fig.suptitle("Impact de la taille de la population sur la convergence et le temps d'exécution (moyenne sur 10 seeds)")
fig.tight_layout()
plt.grid(True, which='both', axis='both', linestyle='--', alpha=0.5)
plt.savefig('plots/population_size_{}_{}_seeds.png'.format(TARGET_SOLUTION, num_seeds))


# Ratios de mating pool à tester
mating_pool_ratios = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85 ,0.9, 0.95, 1.0]
generations_needed = []
execution_times = []

# Tester chaque ratio
for ratio in mating_pool_ratios:
    generations_accumulated = []
    execution_times_accumulated = []
    
    for seed in seeds:
        ga = GeneticAlgorithm(pop_size=500, pm=0.01, elitism=0.05)
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        generations, fitness, chromosome = ga.run_genetic_algorithm(
            seed=seed, 
            tol=len(TARGET_SOLUTION), 
            display=False, 
            mating_pool_size_ratio=ratio
        )
        end_time = time.time()
        
        # Accumuler les résultats
        generations_accumulated.append(generations)
        execution_times_accumulated.append(end_time - start_time)
    
    # Moyenne sur les seeds
    avg_generations = sum(generations_accumulated) / len(seeds)
    avg_execution_time = sum(execution_times_accumulated) / len(seeds)
    
    generations_needed.append(avg_generations)
    execution_times.append(avg_execution_time)

# Tracer le graphique
fig, ax1 = plt.subplots(figsize=(10, 6))

# Premier axe : nombre de générations
color1 = 'tab:blue'
ax1.set_xlabel("Taille de la mating pool (en fraction de la population)")
ax1.set_ylabel("Nombre de générations nécessaires", color=color1)
ax1.plot(mating_pool_ratios, generations_needed, marker='o', linestyle='-', color=color1, label="Nombre de générations")
ax1.tick_params(axis='y', labelcolor=color1)

# Second axe : temps d'exécution
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel("Temps d'exécution (s)", color=color2)
ax2.plot(mating_pool_ratios, execution_times, marker='o', linestyle='--', color=color2, label="Temps d'exécution")
ax2.tick_params(axis='y', labelcolor=color2)

# Titre et légendes
fig.suptitle("Impact de la taille de la mating pool sur la convergence et le temps d'exécution")
fig.tight_layout()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.savefig('plots/mating_pool_size_{}_{}_seeds.png'.format(TARGET_SOLUTION, num_seeds))


# Taux de mutation à tester
mutation_rates = [0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2]
generations_needed = []
execution_times = []

# Tester chaque taux de mutation
for pm in mutation_rates:
    generations_accumulated = []
    execution_times_accumulated = []
    
    for seed in seeds:
        ga = GeneticAlgorithm(pop_size=500, pm=pm, elitism=0.05)
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        generations, fitness, chromosome = ga.run_genetic_algorithm(
            seed=seed, 
            tol=len(TARGET_SOLUTION), 
            display=False
        )
        end_time = time.time()
        
        # Accumuler les résultats
        generations_accumulated.append(generations)
        execution_times_accumulated.append(end_time - start_time)
    
    # Moyenne sur les seeds
    avg_generations = sum(generations_accumulated) / len(seeds)
    avg_execution_time = sum(execution_times_accumulated) / len(seeds)
    
    generations_needed.append(avg_generations)
    execution_times.append(avg_execution_time)


# Tracer le graphique
fig, ax1 = plt.subplots(figsize=(10, 6))

# Premier axe : nombre de générations
color1 = 'tab:blue'
ax1.set_xlabel("Taux de mutation")
ax1.set_xscale("log")  # Échelle logarithmique pour l'axe x
ax1.set_ylabel("Nombre de générations nécessaires", color=color1)
ax1.plot(mutation_rates, generations_needed, marker='o', linestyle='-', color=color1, label="Nombre de générations")
ax1.tick_params(axis='y', labelcolor=color1)

# Second axe : temps d'exécution
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel("Temps d'exécution (s)", color=color2)
ax2.plot(mutation_rates, execution_times, marker='o', linestyle='--', color=color2, label="Temps d'exécution")
ax2.tick_params(axis='y', labelcolor=color2)

# Titre et légendes
fig.suptitle("Impact du taux de mutation sur la convergence et le temps d'exécution")
fig.tight_layout()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.savefig('plots/mutation_rate_{}_{}_seeds.png'.format(TARGET_SOLUTION, num_seeds))


# Taux d'élitisme à tester
elitism_rates = [0.002, 0.01, 0.02, 0.04, 0.1, 0.2, 0.5]
generations_needed = []
execution_times = []

# Tester chaque taux d'élitisme
for elitism in elitism_rates:
    generations_accumulated = []
    execution_times_accumulated = []
    
    for seed in seeds:
        ga = GeneticAlgorithm(pop_size=500, pm=0.01, elitism=elitism)
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        generations, fitness, chromosome = ga.run_genetic_algorithm(
            seed=seed, 
            tol=len(TARGET_SOLUTION), 
            display=False
        )
        end_time = time.time()
        
        # Accumuler les résultats
        generations_accumulated.append(generations)
        execution_times_accumulated.append(end_time - start_time)
    
    # Moyenne sur les seeds
    avg_generations = sum(generations_accumulated) / len(seeds)
    avg_execution_time = sum(execution_times_accumulated) / len(seeds)
    
    generations_needed.append(avg_generations)
    execution_times.append(avg_execution_time)

# Tracer le graphique
fig, ax1 = plt.subplots(figsize=(10, 6))

# Premier axe : nombre de générations
color1 = 'tab:blue'
ax1.set_xlabel("Taux d'élitisme")
ax1.set_xscale("log")  # Échelle logarithmique pour l'axe x
ax1.set_ylabel("Nombre de générations nécessaires", color=color1)
ax1.plot(elitism_rates, generations_needed, marker='o', linestyle='-', color=color1, label="Nombre de générations")
ax1.tick_params(axis='y', labelcolor=color1)

# Second axe : temps d'exécution
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel("Temps d'exécution (s)", color=color2)
ax2.plot(elitism_rates, execution_times, marker='o', linestyle='--', color=color2, label="Temps d'exécution")
ax2.tick_params(axis='y', labelcolor=color2)

# Titre et légendes
fig.suptitle("Impact du taux d'élitisme sur la convergence et le temps d'exécution")
fig.tight_layout()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.savefig('plots/elitism_rate_{}_{}_seeds.png'.format(TARGET_SOLUTION, num_seeds))



# Comparaison entre simple et double crossover
crossover_types = ["single", "double"]
generations_needed_crossover = {ctype: [] for ctype in crossover_types}
execution_times_crossover = {ctype: [] for ctype in crossover_types}

# Tester chaque méthode de crossover
for ctype in crossover_types:
    for pop_size in population_sizes:
        generations_accumulated = []
        execution_times_accumulated = []

        for seed in seeds:
            ga = GeneticAlgorithm(pop_size=pop_size)

            # Mesurer le temps d'exécution
            start_time = time.time()
            generations, fitness, chromosome = ga.run_genetic_algorithm(
                seed=seed, 
                tol=len(TARGET_SOLUTION), 
                display=False, 
                mating_pool_size_ratio=0.5,
                crossover_type=ctype  # Spécifier le type de crossover
            )
            end_time = time.time()
            
            generations_accumulated.append(generations)
            execution_times_accumulated.append(end_time - start_time)
        
        # Moyenne sur les seeds
        avg_generations = sum(generations_accumulated) / len(seeds)
        avg_execution_time = sum(execution_times_accumulated) / len(seeds)
        
        generations_needed_crossover[ctype].append(avg_generations)
        execution_times_crossover[ctype].append(avg_execution_time)

# Tracer les graphiques comparatifs
fig, ax1 = plt.subplots(figsize=(10, 6))

# Nombre de générations
for ctype in crossover_types:
    ax1.plot(population_sizes, generations_needed_crossover[ctype], marker='o', linestyle='-', label=f"Generations ({ctype})")

ax1.set_xlabel("Taille de la population")
ax1.set_ylabel("Nombre de générations nécessaires")
ax1.legend(loc="upper left")

# Temps d'exécution
ax2 = ax1.twinx()
for ctype in crossover_types:
    ax2.plot(population_sizes, execution_times_crossover[ctype], marker='o', linestyle='--', label=f"Temps ({ctype})")

ax2.set_ylabel("Temps d'exécution (s)")
ax2.legend(loc="upper right")

# Titre et légendes
fig.suptitle("Comparaison des méthodes de crossover : simple vs double")
fig.tight_layout()
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('plots/population_comparison_single_double_{}_{}_seeds.png'.format(TARGET_SOLUTION, num_seeds))

