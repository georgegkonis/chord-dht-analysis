import unittest
from tests.test_chord_join import TestChordJoin
from tests.test_chord_insert import TestChordInsert
from tests.test_chord_leave import TestChordLeave
from tests.test_chord_lookup import TestChordLookup
from tests.test_chord_node import TestChordNode


def suite():
    test_suite = unittest.TestSuite()

    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChordJoin))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChordInsert))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChordLeave))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChordLookup))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestChordNode))

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
