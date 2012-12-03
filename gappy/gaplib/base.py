import random


class Agent(object):
    def __init__(self, capacity, work_units, costs):
        self.capacity = capacity
        self.work_units = work_units
        self.costs = costs


class AgentAggregateInfo(object):
    def __init__(self, agent, assignments, work_total, cost_total):
        self.agent = agent
        self.assignments = assignments
        self.work_total = work_total
        self.excess_work = work_total - agent.capacity
        self.cost_total = cost_total

    def add_assignment(self, index):
        work_units = self.agent.work_units[index]
        self.work_total += work_units
        self.excess_work += work_units
        self.cost_total += self.agent.costs[index]
        self.assignments.append(index)

    def remove_assignment(self, index):
        work_units = self.agent.work_units[index]
        self.work_total -= work_units
        self.excess_work -= work_units
        self.cost_total -= self.agent.costs[index]
        self.assignments.remove(index)

    @property
    def has_excess_work(self):
        return self.excess_work > 0


class Solution(object):
    def __init__(self, agents, assignments):
        self.agents = agents
        self.assignments = assignments
        self.assignment_count = len(assignments)
        self._agent_aggregates = self._get_aggregate_info()
        self._excess_work_agents = self._get_excess_work_agents()

    def _update_excess_status(self, agent_aggregate):
        agent_set = {agent_aggregate.agent}
        if agent_aggregate.has_excess_work:
            self._excess_work_agents |= agent_set
        else:
            self._excess_work_agents -= agent_set

    def _reassign(self, index, new_agent):
        new_agent_agg = self._agent_aggregates[new_agent]
        new_agent_agg.add_assignment(index)
        self._update_excess_status(new_agent_agg)

        old_agent = self.assignments[index]
        old_agent_agg = self._agent_aggregates[old_agent]
        old_agent_agg.remove_assignment(index)
        self._update_excess_status(old_agent_agg)

        self.assignments[index] = new_agent

    def _get_aggregate_info(self):
        aggregates = {}
        for agent in self.agents:
            aggregates[agent] = AgentAggregateInfo(agent, [], 0, 0)

        for i in xrange(self.assignment_count):
            agent = self.assignments[i]
            aggregates[agent].add_assignment(i)

        return aggregates

    def _get_excess_work_agents(self):
        return set(agg.agent for agg in self._agent_aggregates.values()
                   if agg.has_excess_work)

    @property
    def total_cost(self):
        return sum(agg.cost_total for agg in self._agent_aggregates.values())

    @classmethod
    def cross_over(self, parent1, parent2):
        random_parent = lambda: random.choice((parent1, parent2))
        assignments = [random_parent().assignments[i]
                       for i in xrange(parent1.assignment_count)]

        return Solution(parent1.agents, assignments)

    def mutate(self, mutations):
        if mutations > self.assignment_count:
            raise ValueError("More mutations specified than there are "
                             "chromosomes to mutate.")

        mutated_indices = set()
        random_agent = lambda: random.choice(self.agents)

        new_assignments = list(a for a in self.assignments)
        max_index = self.assignment_count - 1
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

    @property
    def satisfies_constraint(self):
        return not self._excess_work_agents

    def repair(self):
        excess_or_zero = lambda delta: delta if delta > 0 else 0
        while self._excess_work_agents:
            # Find a random excess agent.
            excess_agent = random.sample(self._excess_work_agents, 1)[0]

            # Find a random task for that agent.
            excess_agent_aggregate = self._agent_aggregates[excess_agent]
            excess_agent_task_index = random.choice(
                excess_agent_aggregate.assignments)

            excess_agent_task_work = (
                excess_agent.work_units[excess_agent_task_index])

            # Create a random swap scenario.
            swap_agent = random.choice(self.agents)
            swap_agent_excess = self._agent_aggregates[swap_agent].excess_work
            swap_task_index = random.choice(xrange(self.assignment_count))
            swap_task_work = swap_agent.work_units[swap_task_index]

            # Make note of excesses before swap.
            total_excess_before_swap = (
                excess_or_zero(excess_agent_aggregate.excess_work)
                + excess_or_zero(swap_agent_excess)
            )

            # Play out swap scenario and swap if excess is not increased.
            is_shift = excess_agent_task_index == swap_task_index
            if is_shift:
                total_excess_after_swap = (
                    (
                        excess_or_zero(excess_agent_aggregate.excess_work
                                       - excess_agent_task_work)
                    ) + (
                        excess_or_zero(swap_agent_excess
                                       + swap_task_work)
                    )
                )

                if total_excess_after_swap < total_excess_before_swap:
                    self._reassign(excess_agent_task_index, swap_agent)

            else:
                total_excess_after_swap = (
                    excess_or_zero(
                        swap_agent_excess
                        - swap_task_work
                        + swap_agent.work_units[excess_agent_task_index]
                    ) + excess_or_zero(
                        excess_agent_aggregate.excess_work
                        - excess_agent_task_work
                        + excess_agent.work_units[swap_task_index]
                    )
                )

                if total_excess_after_swap < total_excess_before_swap:
                    self._reassign(swap_task_index, excess_agent)
                    self._reassign(excess_agent_task_index, swap_agent)

    @classmethod
    def generate_random(cls, agents):
        task_count = len(agents[0].costs)
        assignments = []
        for task in xrange(task_count):
            random_agent = random.choice(agents)
            assignments.append(random_agent)
        solution = Solution(agents, assignments)
        solution.repair()
        return solution
