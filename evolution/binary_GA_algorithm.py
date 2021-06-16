import numpy as np


class SequentialGA:
    def __init__(
            self,
            initial_genetic_material,
            population_size,
            selector,
            evaluator,
            recombinator,
            mutator,
            same_agent_breeding=False
    ):
        self.population = []
        self.population_size = population_size
        self.selector = selector
        self.same_agent_breeding = same_agent_breeding
        self.generation_count = 0

        for dna_sequence in initial_genetic_material:
            agent = Agent(self.name_agent(), dna_sequence, evaluator, recombinator, mutator)
            self.population.append(agent)

    def run_evolution(self):
        new_population = []
        # evaluate fitness of population
        for agent in self.population:
            agent.fitness()

        # run elitism add top x percent of elits to the next gen immediately

        # select and breed population
        while len(new_population) < self.population_size:
            parent1, parent2 = self.breed()
            child = parent1.mate(parent2)
            child.mutate()
            child.name = self.name_agent()
            new_population.append(child)

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
        name = f'gen:{self.generation_count}:{seq}'
        return name


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

    def mate(self):
        pass
