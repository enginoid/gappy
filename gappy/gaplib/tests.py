import unittest
from gappy.gaplib.base import Agent


class AgentTest(unittest.TestCase):

    def setUp(self):
        self.poorAgent = Agent(capacity=5, work_units=(5, 10), costs=(2, 6))

    def testConstruction(self):
        self.assertEqual(self.poorAgent.capacity, 5)
        self.assertEqual(self.poorAgent.work_units[1], 10)
        self.assertEqual(self.poorAgent.costs[1], 6)
