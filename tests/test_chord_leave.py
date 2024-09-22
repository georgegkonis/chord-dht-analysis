import unittest

from src.chord_dht.chord import Chord


class TestChordLeave(unittest.TestCase):
    def setUp(self):
        self.m = 5
        self.chord = Chord(self.m)

    def test_leave_one_success(self):
        self.chord.join(0)
        self.chord.leave(0)

        nodes = self.chord.nodes

        self.assertEqual(0, len(self.chord))
        self.assertNotIn(0, nodes)
