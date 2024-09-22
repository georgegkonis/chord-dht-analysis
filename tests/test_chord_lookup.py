import unittest

from src.chord_dht.chord import Chord


class TestChordLookup(unittest.TestCase):
    def setUp(self):
        m = 2
        chord = Chord(m)

        for i in range(chord.m ** 2):
            chord.join(i)

        self.chord = chord

    def test_lookup(self):
        self.chord.insert('a', 'val_a')
        self.chord.insert('b', 'val_b')
        self.chord.insert('c', 'val_c')

        self.assertEqual(['val_a'], self.chord.lookup('a'))
        self.assertEqual(['val_b'], self.chord.lookup('b'))
        self.assertEqual(['val_c'], self.chord.lookup('c'))
