import random


class Tournament:

    def __init__(self, tournament_size, with_replacement=False):
        self.tournament_size = tournament_size
        self.with_replacement = with_replacement

    def __call__(self, population):

        if self.with_replacement is True:
            group = random.choices(population, k=self.tournament_size)
        else:
            group = random.sample(population, k=self.tournament_size)

        fittest_agent = group.pop()
        for agent in group:
            if agent.fitness_score > fittest_agent.fitness_score:
                fittest_agent = agent

        return fittest_agent

