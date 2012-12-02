import random


class Agent(object):
    def __init__(self, capacity, work_units, costs):
        if (0 in work_units) or (0 in costs):
            raise ValueError("Task costs or work units can't be zero.")

        self.capacity = capacity
        self.work_units = work_units
        self.costs = costs

    def get_work_to_cost_ratio(self, task_index):
        return float(self.work_units[task_index]) / self.costs[task_index]


class Solution(object):
    def __init__(self, agents, assignments):
        self.agents = agents
        self.assignments = list(assignments)
        self._agent_aggregate_info = None

    def _clear_aggregate_info(self):
        self._agent_aggregate_info = None

    def _get_agent_aggregate_info(self):
        if self._agent_aggregate_info is None:
            empty_aggregate_dict = lambda: {'work_total': 0,
                                            'assignments': []}

            aggregates = dict((agent, empty_aggregate_dict())
                              for agent in self.agents)

            for i in xrange(len(self.assignments)):
                agent = self.assignments[i]
                aggregates[agent]['work_total'] += agent.work_units[i]
                aggregates[agent]['assignments'].append(i)

            self._agent_aggregate_info = aggregates
        return self._agent_aggregate_info

    def _get_agent_excess_work(self, agent):
        work_total = self._get_agent_aggregate_info()[agent]['work_total']
        delta = work_total - agent.capacity
        return delta

    def _get_agents_with_excess_work(self):
        agents = []
        for agent, aggregate_info in self._get_agent_aggregate_info().items():
            if aggregate_info['work_total'] > agent.capacity:
                agents.append(agent)
        return agents

    @property
    def assignment(self):
        return self._assignments

    @property
    def total_cost(self):
        return sum(self.assignments[i].costs[i]
                   for i in xrange(len(self.assignments)))

    def get_total_agent_work(self, agent):
        return self._get_agent_aggregate_info()[agent]['work_total']

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

    def repair(self):
        excess_or_zero = lambda delta: delta if delta > 0 else 0
        excess_work_agents = self._get_agents_with_excess_work()
        while excess_work_agents:
            # Find a random excess agent.
            excess_agent = random.choice(excess_work_agents)

            # Find a random task for that agent.
            excess_agent_info = self._get_agent_aggregate_info()[excess_agent]
            excess_agent_task_indices = excess_agent_info['assignments']
            excess_agent_task_index = random.choice(excess_agent_task_indices)
            excess_agent_task_work = (excess_agent
                                      .work_units[excess_agent_task_index])
            excess_agent_excess = self._get_agent_excess_work(excess_agent)

            # Create a random swap scenario.
            swap_agent = random.choice(self.agents)
            swap_agent_excess = self._get_agent_excess_work(swap_agent)
            swap_task_index = random.choice(xrange(len(self.assignments)))
            swap_task_work = swap_agent.work_units[swap_task_index]

            # Make note of excesses before swap.
            total_excess_before_swap = (
                excess_or_zero(excess_agent_excess)
                + excess_or_zero(swap_agent_excess)
            )

            # Play out swap scenario and swap if excess is not increased.
            is_shift = excess_agent_task_index == swap_task_index
            if is_shift:
                total_excess_after_swap = (
                    (
                        excess_or_zero(excess_agent_excess
                                       - excess_agent_task_work)
                    ) + (
                        excess_or_zero(swap_agent_excess
                                       + swap_task_work)
                    )
                )

                if total_excess_after_swap <= total_excess_before_swap:
                    self.assignments[excess_agent_task_index] = swap_agent
                    self._clear_aggregate_info()

            else:
                total_excess_after_swap = (
                    excess_or_zero(
                        swap_agent_excess
                        - swap_task_work
                        + swap_agent.work_units[excess_agent_task_index]
                    ) + excess_or_zero(
                        excess_agent_excess
                        - excess_agent_task_work
                        + excess_agent.work_units[swap_task_index]
                    )
                )

                if total_excess_after_swap <= total_excess_before_swap:
                    a = self.assignments
                    a[swap_task_index], a[excess_agent_task_index] = (
                        a[excess_agent_task_index], a[swap_task_index])
                    self._clear_aggregate_info()

            excess_work_agents = self._get_agents_with_excess_work()
