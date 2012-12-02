import unittest
from gappy.gaplib.base import Agent, Solution

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


class SolutionTest(unittest.TestCase):

    def setUp(self):
        agents = (get_good_agent(), get_poor_agent())

        self.poorAgentSolution = Solution(
            agents=agents, assignments=(0, 0))

        self.goodAgentSolution = Solution(
            agents=agents, assignments=(1, 1))

    def testConstruction(self):
        self.assertEqual(self.goodAgentSolution.assignments[1], 1)
