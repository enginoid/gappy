import unittest
from ..ga import GeneticAlgorithm
from os.path import dirname, join, abspath


class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        self.ga = self.get_instance_by_filename('D3-15.dat')

    def get_instance_by_filename(self, filename):
        absolute_dir = dirname(abspath(__file__))
        with open(join(absolute_dir, filename), 'r') as f:
            ga = GeneticAlgorithm.from_file(f)
        return ga

    def testFromFile(self):
        ga = self.ga
        agent = ga.agents[2]
        self.assertEqual(len(ga.agents), 3)
        self.assertEqual(len(agent.costs), 15)
        self.assertEqual(agent.capacity, 290)
        self.assertEqual(agent.work_units[14], 65)
        self.assertEqual(agent.costs[14], 53)

    def testFromInvalidFile(self):
        with self.assertRaises(RuntimeError):
            self.get_instance_by_filename('D3-15-corrupt.dat')

    def testGenerateRandomSolutions(self):
        self.ga.generate_random_solutions(100)
        self.assertEqual(100, len(self.ga.solution_pool))

    def testAddGeneration(self):
        self.ga.generate_random_solutions(100)
        self.ga.double_population()
        self.assertEqual(200, len(self.ga.solution_pool))

    def testHalvePopulation(self):
        self.ga.generate_random_solutions(100)
        self.ga.halve_population()
        self.assertEqual(50, len(self.ga.solution_pool))
