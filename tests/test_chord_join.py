import unittest

from src.chord_dht.chord import Chord


class TestChordJoin(unittest.TestCase):
    def setUp(self):
        self.m = 3
        self.chord = Chord(self.m)

    def test_join_one_success(self):
        self.chord.join(0)

        nodes = self.chord.nodes

        self.assertEqual(1, len(self.chord))
        self.assertIn(0, nodes)

        self.assertEqual(0, nodes[0].id)
        self.assertEqual(0, nodes[0].successor.id)
        self.assertEqual(0, nodes[0].predecessor.id)
        self.assertListEqual([0, 0, 0], [finger.id for finger in nodes[0].fingers])

    def test_join_two_success(self):
        self.chord.join(0)
        self.chord.join(1)

        nodes = self.chord.nodes

        self.assertEqual(2, len(self.chord))
        self.assertIn(0, nodes)
        self.assertIn(1, nodes)

        self.assertEqual(0, nodes[0].id)
        self.assertEqual(1, nodes[0].successor.id)
        self.assertEqual(1, nodes[0].predecessor.id)
        self.assertListEqual([1, 0, 0], [finger.id for finger in nodes[0].fingers])

        self.assertEqual(1, nodes[1].id)
        self.assertEqual(0, nodes[1].successor.id)
        self.assertEqual(0, nodes[1].predecessor.id)
        self.assertListEqual([0, 0, 0], [finger.id for finger in nodes[1].fingers])

    def test_join_three_success(self):
        self.chord.join(0)
        self.chord.join(1)
        self.chord.join(2)

        nodes = self.chord.nodes

        self.assertEqual(3, len(self.chord))
        self.assertIn(0, nodes)
        self.assertIn(1, nodes)
        self.assertIn(2, nodes)

        self.assertEqual(0, nodes[0].id)
        self.assertEqual(1, nodes[0].successor.id)
        self.assertEqual(2, nodes[0].predecessor.id)
        self.assertListEqual([1, 2, 0], [finger.id for finger in nodes[0].fingers])

        self.assertEqual(1, nodes[1].id)
        self.assertEqual(2, nodes[1].successor.id)
        self.assertEqual(0, nodes[1].predecessor.id)
        self.assertListEqual([2, 0, 0], [finger.id for finger in nodes[1].fingers])

        self.assertEqual(2, nodes[2].id)
        self.assertEqual(0, nodes[2].successor.id)
        self.assertEqual(1, nodes[2].predecessor.id)
        self.assertListEqual([0, 0, 0], [finger.id for finger in nodes[2].fingers])

    def test_join_invalid_id(self):
        with self.assertRaises(ValueError):
            self.chord.join(-1)

        with self.assertRaises(ValueError):
            self.chord.join(2 ** self.m)

    def test_join_duplicate_id(self):
        """
        Test joining the same node twice should raise a ValueError.
        """
        self.chord.join(0)

        with self.assertRaises(ValueError):
            self.chord.join(0)
