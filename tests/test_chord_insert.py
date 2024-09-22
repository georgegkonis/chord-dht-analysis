import unittest

import src.chord_dht.chord_utils
from src.chord_dht.chord import Chord


class TestChordInsert(unittest.TestCase):
    def setUp(self):
        chord = Chord(2)

        for i in range(chord.m ** 2):
            chord.join(i)

        self.chord = chord

    def test_insert(self):
        self.chord.insert('a', 'val_a')
        self.chord.insert('b', 'val_b')
        self.chord.insert('c', 'val_c')

        self.assertEqual(['val_a'], self.chord.lookup('a'))
        self.assertEqual(['val_b'], self.chord.lookup('b'))
