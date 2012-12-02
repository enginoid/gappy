import random


class Agent(object):
    def __init__(self, capacity, work_units, costs):
        self.capacity = capacity
        self.work_units = work_units
        self.costs = costs


class Solution(object):
    def __init__(self, agents, assignments):
        self.agents = agents
        self.assignments = assignments

    @property
    def total_cost(self):
        return sum(self.assignments[i].costs[i]
                   for i in xrange(len(self.assignments)))

    def get_total_agent_work(self, agent):
        return sum(self.assignments[i].work_units[i]
                   for i in xrange(len(self.assignments))
                   if self.assignments[i] == agent)

    @classmethod
    def cross_over(self, parent1, parent2):
        assert len(parent1.assignments) == len(parent2.assignments)

        random_parent = lambda: random.choice((parent1, parent2))
        assignments = tuple(random_parent().assignments[i]
                            for i in xrange(len(parent1.assignments)))

        return Solution(parent1.agents, assignments)

    def mutate(self, mutations):
        if mutations > len(self.assignments):
            raise ValueError("More mutations specified than there are "
                             "chromosomes to mutate.")

        mutated_indices = set()
        random_agent = lambda: random.choice(self.agents)

        new_assignments = list(a for a in self.assignments)
        max_index = len(new_assignments) - 1
        for _ in xrange(mutations):
            while True:
                index = random.randint(0, max_index)
                if not index in mutated_indices:
                    current_agent = new_assignments[index]
                    new_agent = random_agent()
                    if current_agent != new_agent:
                        new_assignments[index] = new_agent
                        mutated_indices.add(index)
                        break

        return Solution(self.agents, new_assignments)
