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
