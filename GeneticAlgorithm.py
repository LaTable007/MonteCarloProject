import random

ALLELE_POOL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !.,?"
TARGET_SOLUTION = "Hellow World!"



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
        prob_mutation = 5
        mutated_chromosome = individual
        for i in range(len(mutated_chromosome)):
            if random.randint(0, 100) < prob_mutation:
                mutated_chromosome = mutated_chromosome[:i] + "".join(random.choices(self.allele_pool)) + mutated_chromosome[i+1:]
        return self.Individual(mutated_chromosome)
    
    def selection(self, population):
        """
        :param population : A list of instances of the class Individuals
        :return: The mating pool constructed from
                the 50% fittest individuals in the population
        """
        mating_pool = list()
        sortedPopulation = sorted(population, key=lambda individual: individual.get_fitness(), reverse=True)
        for i in range(int(self.pop_size/2)):
            mating_pool.append(sortedPopulation[i])
        return mating_pool

    def create_offspring(self, parent1, parent2):
        """
        :param parent1: An instance of the class Individual
        :param parent2: An instance of the class Individual
        :return: Two chromosomes/strings created by
                single-point crossover of the parents'
                chromosomes
        """
        indexCrossover = random.randint(0, len(TARGET_SOLUTION))
        chromosome1, chromosome2 = parent1.get_chromosome(), parent2.get_chromosome()

        offspring1 = chromosome1[:indexCrossover] + chromosome2[indexCrossover:]
        offspring2 = chromosome2[:indexCrossover] + chromosome1[indexCrossover:]

        return (offspring1,offspring2)
        
    
    def run_genetic_algorithm(self, seed, 
                              tol = 0.0,
                              display = True):
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
            mating_pool = self.selection(population)

            
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
                    offspring1, offspring2 = self.create_offspring(parent1, parent2)

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

test = GeneticAlgorithm()

test.run_genetic_algorithm(1, len(TARGET_SOLUTION))
