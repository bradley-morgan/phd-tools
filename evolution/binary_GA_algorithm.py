import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class SequentialGA:
    def __init__(
            self,
            initial_genetic_material,
            population_size,
            selector,
            evaluator,
            recombinator,
            mutator,
            target_metric=None,
            evolution_steps=100,
            same_agent_breeding=False,
            plot_metrics=True
    ):
        self.population = []
        self.population_size = population_size
        self.selector = selector
        self.evaluator = evaluator
        self.recombinator = recombinator
        self.mutator = mutator
        self.same_agent_breeding = same_agent_breeding
        self.evolution_steps = evolution_steps
        self.target_metric = target_metric

        self.generation_count = 0
        self.best_agent_history = []
        self.mean_fitness_history = []
        self.mean_weight_history = []
        self.best_weight_history = []
        self.lowest_weight_history = []
        self.mean_packed_item_history = []
        self.best_packed_item_history = []
        self.best_agent = None

        for dna_sequence in initial_genetic_material:
            agent = Agent(self.name_agent(), dna_sequence, evaluator, recombinator, mutator)
            self.population.append(agent)

    def run_evolution(self):

        for generation in range(self.evolution_steps):

            self.generation_count = generation
            new_population = []
            # evaluate fitness of population
            best_fitness = 0
            mean_fitness = 0
            mean_weight = 0
            lowest_weight = None
            best_weight = 0
            mean_packed_items = 0
            best_packed_items = 0

            for agent in self.population:
                fitness, weight, packed_items = agent.fitness()
                mean_fitness += fitness
                mean_weight += weight

                # max fitness
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_weight = weight
                    self.best_agent = agent
                    best_packed_items = packed_items

                # min weight
                if lowest_weight is None:
                    lowest_weight = weight

                elif weight < lowest_weight:
                    lowest_weight = weight

                mean_packed_items += packed_items

            mean_weight = mean_weight / len(self.population)
            mean_fitness = mean_fitness / len(self.population)
            mean_packed_items = mean_packed_items / len(self.population)

            self.mean_weight_history.append(mean_weight)
            self.best_weight_history.append(best_weight)
            self.lowest_weight_history.append(lowest_weight)
            self.mean_fitness_history.append(mean_fitness)
            self.best_agent_history.append(best_fitness)
            self.best_packed_item_history.append(best_packed_items)
            self.mean_packed_item_history.append(mean_packed_items)

            print(f'Generation: {self.generation_count}. Best fitness: {best_fitness}'
                  f'  Mean fitness: {mean_fitness}  Best weight: {best_weight}  Mean weight: {mean_weight}')

            # terminate early if target metric has been reached
            if self.target_metric is not None and best_fitness >= self.target_metric:
                print(f'Target Metric Exceeded - best fitness: {best_fitness} mean fitness {mean_fitness}')
                break

            # run elitism add top x percent of elits to the next gen immediately

            # select and breed population
            while len(new_population) < self.population_size:
                parent1, parent2 = self.breed()
                child_dna = parent1.mate(parent2)
                child = Agent(self.name_agent(), child_dna, self.evaluator, self.recombinator, self.mutator)
                child.mutate()
                new_population.append(child)

            self.population = new_population

    def breed(self):

        parent_agent1 = None
        parent_agent2 = None

        if self.same_agent_breeding:
            valid = False
            while valid is False:
                parent_agent1 = self.selector(self.population)
                parent_agent2 = self.selector(self.population)
                if parent_agent1.name != parent_agent2.name:
                    valid = True
        else:
            parent_agent1 = self.selector(self.population)
            parent_agent2 = self.selector(self.population)

        return parent_agent1, parent_agent2

    def name_agent(self):
        nums = np.random.randint(0, 127, 8)
        seq = []
        for n in nums:
            seq.append(chr(n))
        seq = ''.join(seq)
        name = f'gen:{self.generation_count+1}:{seq}'
        return name

    def generate_plots(self, weight_limit):
        sns.set()
        plt.figure(1)
        plt.plot(self.mean_fitness_history)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Mean fitness')
        plt.title('Mean Fitness')

        plt.figure(2)
        plt.plot(self.best_agent_history)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Best fitness')
        plt.title('Best Fitness')

        plt.figure(3)
        plt.plot(self.mean_weight_history)
        plt.plot([weight_limit] * self.evolution_steps)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Mean Weight')
        plt.title('Mean Weight')
        plt.legend(["Data", "Weight Limit"])

        plt.figure(4)
        plt.plot(self.lowest_weight_history)
        plt.plot([weight_limit] * self.evolution_steps)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Lowest Weight')
        plt.title('Lowest Weight')
        plt.legend(["Data", "Weight Limit"])


        plt.figure(5)
        plt.plot(self.best_weight_history)
        plt.plot([weight_limit] * self.evolution_steps)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Weight of the best agent per evolution step')
        plt.title('Best agent weight')
        plt.legend(["Data", "Weight Limit"])

        plt.figure(6)
        plt.plot(self.best_packed_item_history)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Number of Packed Items')
        plt.title('The Number of items the best agent packs')

        plt.figure(7)
        plt.plot(self.mean_packed_item_history)
        plt.xlabel('Evolution Steps')
        plt.ylabel('Number of Packed Items')
        plt.title('Mean Number of items packed')

        plt.show()


class Agent:
    def __init__(self, name, genetic_material, evaluator, recombinator, mutator):
        self.name = name
        self.genetic_material = genetic_material
        self.evaluator = evaluator
        self.recombinator = recombinator
        self.mutator = mutator
        self.fitness_score = None

    def fitness(self):
        self.fitness_score = self.evaluator(self.genetic_material)
        return self.fitness_score

    def mutate(self):
        self.genetic_material = self.mutator(self.genetic_material)

    def mate(self, mating_partner):
        return self.recombinator(self.genetic_material, mating_partner.genetic_material)
