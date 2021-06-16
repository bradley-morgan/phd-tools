from test_problems import KnapSack
from evolution.binary_GA_algorithm import SequentialGA
from evolution.selector import Tournament
from evolution.recombinator import RUniform
from evolution.mutator import MUniform
# problem params

# Everything is specified within the limits
weight_average = 20
weight_spread = 10
value_average = 20
value_spread = 10
weight_limit = 700
total_items = 10

# GA params
population_size = 500
evolution_steps = 100
mutation_rate = 0.01
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
knapsack.add_variable(name="scarcity", value_type='pos', value_strength=0.8, weight_type='none', weight_strength=0.0)
knapsack.add_variable(name="size", value_type='pos', value_strength=0.4, weight_type='pos', weight_strength=0.7)
knapsack.add_variable(name="brittleness", value_type='neg', value_strength=0.4, weight_type='none', weight_strength=0.0)
knapsack.add_variable(name="popularity", value_type='pos', value_strength=0.6, weight_type='none', weight_strength=0.0)
knapsack.add_variable(name="density", value_type='pos', value_strength=0.1, weight_type='pos', weight_strength=0.9)

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
    plot_metrics=True
)

mother_nature.run_evolution()




