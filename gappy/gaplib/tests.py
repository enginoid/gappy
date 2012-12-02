import unittest
from .base import Agent, Solution

get_poor_agent = lambda: Agent(capacity=5, work_units=(5, 10), costs=(2, 6))
get_good_agent = lambda: Agent(capacity=25, work_units=(10, 20), costs=(1, 3))


class AgentTest(unittest.TestCase):

    def setUp(self):
        self.poorAgent = get_poor_agent()
        self.goodAgent = get_good_agent()

    def testConstruction(self):
        self.assertEqual(self.poorAgent.capacity, 5)
        self.assertEqual(self.poorAgent.work_units[1], 10)
        self.assertEqual(self.poorAgent.costs[1], 6)

    def testZeroWorkUnitsOrCosts(self):
        with self.assertRaises(ValueError):
            Agent(capacity=5, work_units=(0,), costs=(1,))

        with self.assertRaises(ValueError):
            Agent(capacity=5, work_units=(1,), costs=(0,))

    def testWorkToCostRatio(self):
        self.assertEqual(
            (10 / 1.0), self.goodAgent.get_work_to_cost_ratio(0))

        self.assertAlmostEqual(
            (20 / 3.0), self.goodAgent.get_work_to_cost_ratio(1))


class SolutionTest(unittest.TestCase):

    def setUp(self):
        self.goodAgent = get_good_agent()
        self.poorAgent = get_poor_agent()
        self.agents = (self.goodAgent, self.poorAgent)

        self.poorAgentSolution = Solution(
            agents=self.agents, assignments=(self.poorAgent, self.poorAgent))

        self.goodAgentSolution = Solution(
            agents=self.agents, assignments=(self.goodAgent, self.goodAgent))

    def testConstruction(self):
        self.assertEqual(self.goodAgentSolution.assignments[1],
                         self.goodAgent)

    def testGetTotalCost(self):
        self.assertEqual(self.goodAgentSolution.total_cost, 4)
        self.assertEqual(self.poorAgentSolution.total_cost, 8)

    def testGetTotalAgentWork(self):
        self.assertEqual(
            self.goodAgentSolution.get_total_agent_work(self.goodAgent), 30)

        self.assertEqual(
            self.goodAgentSolution.get_total_agent_work(self.poorAgent), 0)

    def testCrossOver(self):
        g = self.goodAgent
        p = self.poorAgent
        possible_assignments = [
            [g, g],
            [p, p],
            [g, p],
            [p, g],
        ]

        max_runs = 100
        runs = 0
        while possible_assignments:
            child = Solution.cross_over(self.poorAgentSolution,
                                        self.goodAgentSolution)

            if child.assignments in possible_assignments:
                possible_assignments.remove(child.assignments)

            runs += 1
            if runs >= max_runs:
                self.fail("Too many crossovers without finding all "
                          "offspring.")

    def testMutate(self):
        self.assertEqual(
            {self.poorAgent},
            set(self.goodAgentSolution.mutate(2).assignments))

        self.assertEqual(
            {self.poorAgent, self.goodAgent},
            set(self.goodAgentSolution.mutate(1).assignments))

        with self.assertRaises(ValueError):
            self.goodAgentSolution.mutate(3)

    def testRepair(self):
        self.poorAgentSolution.repair()
        self.assertEqual([self.poorAgent, self.goodAgent],
                         self.poorAgentSolution.assignments)

    def testGenerateRandom(self):
        random_solution = Solution.generate_random(self.agents)
        self.assertTrue(random_solution.satisfies_constraint)
