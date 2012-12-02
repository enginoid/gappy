import argparse
from ga import GeneticAlgorithm

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filename', metavar='filename', type=unicode,
                    help='a data file to parse and run on')

POPULATION = 100
NUMBER_OF_EVALUATIONS = 5000000

args = parser.parse_args()

def fittest_found_callback(solution, ga):
    agent_indexes = dict((agent, solution.assignments.index(agent))
                         for agent in solution.agents)

    print "best_solution:"
    print "genotype:", ' '.join(str(agent_indexes[agent]) for agent in solution.assignments)
    print "fitness:", solution.total_cost
    print "evaluations_to_best:", ga.evaluations
    print

with open(args.filename) as f:
    ga = GeneticAlgorithm.from_file(f, fittest_found_callback)
    ga.generate_random_solutions(POPULATION)

    evolutions = NUMBER_OF_EVALUATIONS / POPULATION
    for _ in xrange(evolutions):
        ga.evolve_population()

