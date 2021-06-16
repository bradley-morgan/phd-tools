from test_problems import KnapSack
from evolution.binary_GA_algorithm import SequentialGA
from evolution.selector import Tournament
from evolution.recombinator import RUniform
from evolution.mutator import MUniform
import seaborn as sns
import matplotlib.pyplot as plt
# problem params

# Everything is specified within the limits
weight_average = 10
weight_spread = 5
value_average = 20
value_spread = 10
weight_limit = 850
total_items = 100

# GA params
population_size = 800
evolution_steps = 100
mutation_rate = 0.02
tournament_size = 5
tournament_with_replacement = False

knapsack = KnapSack(
    weight_average=weight_average,
    weight_spread=weight_spread,
    value_average=value_average,
    value_spread=value_spread,
    weight_limit=weight_limit,
    total_items=total_items
)

knapsack.generate_problem_space()
population = knapsack.generate_populaton()
population = population(500)

mother_nature = SequentialGA(
    initial_genetic_material=population,
    population_size=population_size,
    evolution_steps=evolution_steps,
    selector=Tournament(tournament_size, with_replacement=tournament_with_replacement),
    evaluator=knapsack.generate_objective_function(),
    recombinator=RUniform(),
    mutator=MUniform(mutation_rate),
    same_agent_breeding=False,
    plot_metrics=True,
    target_metric=1900
)

mother_nature.run_evolution()
mother_nature.generate_plots(weight_limit=weight_limit)
a = 0




