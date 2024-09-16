from __future__ import annotations

import logging
from typing import Optional
from src.chord_dht.chord_utils import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ChordNode:
    """
    A Chord-DHT node.
    :cvar id: The ID of the node.
    :cvar m: The number of bits in the hash space of the Chord ring.
    :cvar successor: The next node in the ring.
    :cvar predecessor: The previous node in the ring.
    :cvar fingers: The finger table of the node.
    :cvar data: The key-value pairs stored in the node.
    """
    id: int
    m: int
    successor: ChordNode
    predecessor: ChordNode
    fingers: list[ChordNode]
    data: dict[str, object]

    def __init__(self, nid: int, m: int):
        """
        A node in a Chord-DHT ring.
        :param nid: The ID of the node.
        :param m: The number of bits in the ID hash space of the Chord ring.
        """
        self.id = nid
        self.m = m
        self.successor = self
        self.predecessor = self
        self.fingers = [self] * self.m
        self.data = {}

    def __str__(self) -> str:
        """
        A string representation of the Chord node.
        :return: A string representation of the Chord node.
        """
        return f"{self.id}: Fingers: {[finger.id for finger in self.fingers]} Next: {self.successor.id} Prev: {self.predecessor.id}"

    def join(self, node: ChordNode):
        """
        Joins the node to the Chord ring.
        :param node: The node to join to the Chord ring.
        """
        if not node:
            raise ValueError("Node to join cannot be None.")

        self.successor = node._find_successor(self.id)
        self.predecessor = self.successor.predecessor

        logging.info(f"Node {self.id} is joining the ring between {self.predecessor.id} and {self.successor.id}...")

        self.successor.predecessor = self
        self.predecessor.successor = self

        self._init_fingers()
        self._update_others_fingers()
        self._pull_data_from_successor()

    def leave(self):
        """
        Leaves the Chord ring.
        """
        logging.info(f"Node {self.id} is leaving the ring...")

        self._replace_in_others_fingers()
        self._push_data_to_successor()

        self.successor.predecessor = self.predecessor
        self.predecessor.successor = self.successor
        self.successor = self.predecessor = self
        self.fingers = [self] * self.m

    def insert(self, key: str, value: object) -> None:
        """
        Inserts a key and its associated value into the Chord ring.
        :param key: The key to insert.
        :param value: The value to insert.
        """
        key_id = hash_id(key, self.m)
        node = self._find_successor(key_id)

        logging.info(f"Inserting key {key} into node {node.id}...")

        node.data[key] = value

    def lookup(self, key: str) -> Optional[object]:
        """
        Looks up a key in the Chord ring and returns the associated value.
        :param key: The key to lookup.
        :return: The value associated with the key, or ``None`` if the key cannot be found.
        """
        key_id = hash_id(key, self.m)
        node = self._find_successor(key_id)

        logging.info(f"Looking up key {key} in node {node.id}...")

        return node.data[key] if key in node.data else None

    def delete(self, key: str) -> None:
        """
        Deletes a key and its associated value from the Chord ring.
        :param key: The key to delete.
        """
        key_id = hash_id(key, self.m)
        node = self._find_successor(key_id)

        logging.info(f"Deleting key {key} from node {node.id}...")

        if key in node.data:
            del node.data[key]

    def _find_closest_finger(self, target_id: int) -> ChordNode:
        """
        Finds the closest finger that precedes the target ID.
        :param target_id: The ID to find the closest finger for.
        :return: The closest finger that precedes the target ID.
        """
        for i in range(self.m - 1, -1, -1):
            finger = self.fingers[i]
            if in_open_range(self.id, target_id, finger.id):
                return finger

        return self

    def _find_successor(self, target_id: int) -> ChordNode:
        """
        Finds the successor node for the target ID.
        :param target_id: The ID to find the successor for.
        :return: The successor node for the target ID.
        """
        if self.id == target_id:
            return self
        if in_right_closed_range(self.id, self.successor.id, target_id):
            return self.successor
        else:
            return self._find_closest_finger(target_id)._find_successor(target_id)

    def _find_predecessor(self, target_id: int) -> ChordNode:
        """
        Finds the predecessor node for the target ID.
        :param target_id: The ID to find the predecessor for.
        :return: The predecessor node for the target ID.
        """
        node = self
        while not in_right_closed_range(node.id, node.successor.id, target_id):
            node = node._find_closest_finger(target_id)
        return node

    def _init_fingers(self):
        """
        Initializes the fingers of the node.
        """
        for i in range(self.m):
            finger_id = (self.id + 2 ** i) % (2 ** self.m)
            self.fingers[i] = self._find_successor(finger_id)

    def _update_others_fingers(self):
        """
        Updates the fingers of other nodes to include this node, if necessary.
        """
        node = self.successor
        while node != self:
            node.fingers = [self._find_successor((node.id + 2 ** i) % (2 ** self.m)) for i in range(self.m)]
            node = node.successor

    def _replace_in_others_fingers(self):
        """
        Replaces this node in the fingers of other nodes with its successor.
        """
        node = self.successor
        while node != self:
            node.fingers = [self.successor if finger == self else finger for finger in node.fingers]
            node = node.successor

    def _pull_data_from_successor(self):
        """
        Pulls all data, this node should store, from its successor node.
        """
        if self == self.successor:
            return

        transfer_data = {
            key: self.successor.data.pop(key)
            for key in list(self.successor.data)
            if in_right_closed_range(self.predecessor.id, self.id, hash_id(key, self.m))
        }

        self.data.update(transfer_data)

    def _push_data_to_successor(self):
        """
        Pushes all data, this node has stored, to its successor node.
        """
        if self == self.successor:
            return

        self.successor.data.update(self.data)
        self.data.clear()
