from Queue import Queue
import random
from gappy.gaplib.base import Agent, Solution


class GeneticAlgorithm(object):
    def __init__(self, agents):
        self.agents = agents
        self.solution_pool = []

    def generate_random_solutions(self, population_size):
        for _ in xrange(population_size):
            solution = Solution.generate_random(self.agents)
            self.solution_pool.append(solution)

    def double_population(self):
        for _ in xrange(len(self.solution_pool)):
            parent1 = random.choice(self.solution_pool)
            parent2 = random.choice(self.solution_pool)
            child = Solution.cross_over(parent1, parent2)
            self.solution_pool.append(child)

    @classmethod
    def from_file(cls, file_obj):
        lines_with_numbers = Queue()
        split_and_strip_ints = lambda line: [int(item.strip())
                                             for item in line.split()]

        for line in file_obj:
            # Ignore comments.
            if line.startswith(';;'):
                continue

            # Ignore empty lines.
            if not line.strip():
                continue

            # For everything else, assume that the line contains whitespace
            # separated ints and add a list of ints to the queue.
            lines_with_numbers.put(split_and_strip_ints(line))

        # Retrieve the ints from the queue in the right order.
        agent_count, task_count, _ = lines_with_numbers.get()
        capacity_constraints = lines_with_numbers.get()
        work_units = [lines_with_numbers.get() for _ in xrange(agent_count)]
        costs = [lines_with_numbers.get() for _ in xrange(agent_count)]

        # Populate agents.
        agents = []
        for i in xrange(agent_count):
            agent = Agent(capacity_constraints[i], work_units[i], costs[i])
            agents.append(agent)

        # Fail if there's more data after we're done parsing.
        if not lines_with_numbers.empty():
            raise RuntimeError("Can't parse data file: unexpected data "
                               "present after parsing.")

        return GeneticAlgorithm(agents)