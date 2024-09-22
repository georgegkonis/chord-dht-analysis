import unittest

from src.chord_dht.chord_node import ChordNode

m = 3


class TestChordNode(unittest.TestCase):

    def setUp(self):
        nodes = [
            ChordNode(0, m),
            ChordNode(1, m),
            ChordNode(2, m),
            ChordNode(4, m),
            ChordNode(6, m)
        ]

        fingers = {
            0: [1, 2, 4],
            1: [2, 4, 6],
            2: [4, 4, 6],
            4: [6, 6, 0],
            6: [0, 0, 2]
        }

        for i, node in enumerate(nodes):
            node.successor = nodes[(i + 1) % len(nodes)]
            node.predecessor = nodes[(i - 1) % len(nodes)]

        self.nodes = dict((node.id, node) for node in nodes)

        for nid, node in self.nodes.items():
            node.fingers = [self.nodes[fid] for fid in fingers[nid]]

    def test_find_successor(self):
        for node_id, node in self.nodes.items():
            s0 = node._find_successor(0)
            self.assertEqual(0, s0.id)

            s1 = node._find_successor(1)
            self.assertEqual(1, s1.id)

            s3 = node._find_successor(3)
            self.assertEqual(4, s3.id)

            s6 = node._find_successor(6)
            self.assertEqual(6, s6.id)

            s7 = node._find_successor(7)
            self.assertEqual(0, s7.id)

    def test_find_predecessor(self):
        for node_id, node in self.nodes.items():
            p0 = node._find_predecessor(0)
            self.assertEqual(6, p0.id)

            p1 = node._find_predecessor(1)
            self.assertEqual(0, p1.id)

            p3 = node._find_predecessor(3)
            self.assertEqual(2, p3.id)

            p6 = node._find_predecessor(6)
            self.assertEqual(4, p6.id)

            p7 = node._find_predecessor(7)
            self.assertEqual(6, p7.id)

    def test_init_fingers(self):
        for node in self.nodes.values():
            fingers = node.fingers
            node._init_fingers()
            self.assertListEqual([f.id for f in node.fingers], [f.id for f in fingers])

    def test_join(self):
        n3 = ChordNode(3, m)
        n3.join(self.nodes[0])

        self.assertEqual(n3.successor.id, 4)
        self.assertEqual(n3.predecessor.id, 2)
        self.assertListEqual([f.id for f in n3.fingers], [4, 6, 0])

        n2 = self.nodes[2]
        self.assertEqual(n2.successor.id, 3)
        self.assertListEqual([f.id for f in n2.fingers], [3, 4, 6])

        n4 = self.nodes[4]
        self.assertEqual(n4.predecessor.id, 3)
        self.assertListEqual([f.id for f in n4.fingers], [6, 6, 0])

        n1 = self.nodes[1]
        self.assertEqual(n1.successor.id, 2)
        self.assertListEqual([f.id for f in n1.fingers], [2, 3, 6])
