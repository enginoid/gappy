import argparse
from ga import GeneticAlgorithm
from gaplib.base import Solution

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('filename', metavar='filename', type=unicode,
                    help='a data file to parse and run on')

parser.add_argument('--population', metavar='population', type=int,
                    default=100, help='how large to keep population')
parser.add_argument('--evaluations', metavar='evaluations', type=int,
    default=10000, help='how many evaluations to run between restarts')
parser.add_argument('--restarts', metavar='restarts', type=int,
    default=10, help='how often to restart from a random point')

args = parser.parse_args()

POPULATION = args.population
NUMBER_OF_EVALUATIONS = args.evaluations
RESTARTS = args.restarts


def agent_indexes(agents):
    return dict((agent, agents.index(agent)) for agent in agents)

def assignment_indexes(solution):
    return [agent_indexes(solution.agents)[agent]
            for agent in solution.assignments]

def assignment_agents(assignment_indices, agents):
    assignments = []
    for i in assignment_indices:
        assignments.append(agents[i])
    return assignments

def fittest_found_callback(solution, ga):
    print "best_solution:"
    print "genotype:", ' '.join(str(i) for i in assignment_indexes(solution))
    print "fitness:", solution.total_cost
    print "feasible:", solution.satisfies_constraint
    print "evaluations_to_best:", ga.evaluations
    print

total_evaluations = 0
top_genotypes = []
for n in xrange(RESTARTS):
    print "restart", n, "out of {0}:".format(RESTARTS)
    print
    with open(args.filename) as f:
        ga = GeneticAlgorithm.from_file(f, fittest_found_callback)
        ga.generate_random_solutions(POPULATION)

        evolutions = NUMBER_OF_EVALUATIONS / POPULATION
        for _ in xrange(evolutions):
            ga.evolve_population()

        indexes = agent_indexes(ga.agents)
        top_genotypes.extend(assignment_indexes(solution)
                             for solution in ga.solution_pool)
        total_evaluations += ga.evaluations

with open(args.filename) as f:
    ga = GeneticAlgorithm.from_file(f, fittest_found_callback)
    ga.solution_pool = [Solution(ga.agents,
                                 assignment_agents(genotype, ga.agents))
                        for genotype in top_genotypes]

    while len(ga.solution_pool) > 10:
        ga.double_population()
        ga.halve_population()
        ga.halve_population()
        print "population:", len(ga.solution_pool)

    print "all done:"
    print "total_evaluations: ", (ga.evaluations + total_evaluations)

    best_solution = sorted(ga.solution_pool, key=lambda s: s.total_cost)[0]
    fittest_found_callback(best_solution, ga)

