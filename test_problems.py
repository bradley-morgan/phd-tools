import numpy as np


class KnapSack:
    def __init__(
            self,
            weight_average: float,
            weight_spread: float,
            value_average: float,
            value_spread: float,
            weight_limit: float,
            total_items: int
    ):

        if weight_average is None:
            raise ValueError(f'weight average is not defined')

        if weight_spread is None:
            raise ValueError('weight spread is not defined')

        if value_average is None:
            raise ValueError(f'value average is not defined')

        if value_spread is None:
            raise ValueError('value spread is not defined')

        if weight_limit is None:
            raise ValueError('weight limit is not defined')

        if total_items is None:
            total_items = 100

        self.weight_average = weight_average
        self.weight_spread = weight_spread
        self.value_average = value_average
        self.value_spread = value_spread
        self.weight_limit = weight_limit
        self.total_items = total_items
        self.population = []
        self.problem_space = []

    def generate_problem_space(self):
        index = 0
        for i in range(0, self.total_items):
            item = self.create_item(name=index)
            self.problem_space.append(item)

    def generate_populaton(self):
        def func(population_size):
            for _ in range(population_size):
                self.population.append(np.random.randint(low=0, high=2, size=len(self.problem_space)))
            return np.array(self.population)

        return lambda population_size: func(population_size)

    def generate_objective_function(self):
        def func(genetic_material):

            fitness = 0
            total_weight = 0
            items_selected = 0
            for i in range(0, len(genetic_material)):
                gene = genetic_material[i]
                if gene == 0:
                    continue

                items_selected += 1
                item = self.problem_space[i]
                fitness += item['value']
                total_weight += item['weight']

                if total_weight > self.weight_limit:
                    fitness = 0
                    break

            return fitness, total_weight, items_selected

        return lambda genetic_material: func(genetic_material)

    def create_item(self, name):

        item = {
            'name': name, 'value': np.random.normal(self.value_average, self.value_spread),
            'weight': np.random.normal(self.weight_average, self.weight_spread)
        }

        if item['value'] < 0:
            item['value'] = 0

        if item['weight'] < 0:
            item['weight'] = 0

        return item
