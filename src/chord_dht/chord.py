from __future__ import annotations

import logging
from src.chord_dht.chord_node import ChordNode


class Chord:
    """
    A Chord-DHT ring.
    :cvar m: The number of bits in the hash space.
    :cvar nodes: A dictionary of nodes in the ring.
    """
    m: int
    nodes: dict[int, ChordNode]

    def __init__(self, m: int):
        """
        Initializes an empty Chord ring.
        :param m: The number of bits in the hash space.
        """
        self.m = m
        self.nodes = {}

    def __len__(self) -> int:
        """
        The size of the Chord ring.
        :return: The number of nodes in the ring.
        """
        return len(self.nodes)

    def __str__(self) -> str:
        """
        A string representation of the Chord ring.
        :return: A string representation of the Chord ring.
        """
        return "\n".join([str(node) for node in self.nodes_in_order])

    @property
    def nodes_in_order(self) -> list[ChordNode]:
        """
        The nodes in the Chord ring in order of ascending node IDs.
        :return: An ordered list of the nodes in the ring.
        """
        return sorted(self.nodes.values(), key=lambda node: node.id)

    def join(self, node_id: int) -> ChordNode:
        """
        Creates a new Chord node and joins it to the Chord ring.
        :param node_id: The ID of the node to join the ring.
        :return: The new Chord node.
        :raises ValueError: If the node ID is out of bounds or already in use.
        """
        if node_id < 0 or node_id >= 2 ** self.m:
            raise ValueError(f"Node ID {node_id} out of bounds for m={self.m}.")

        if node_id in self.nodes:
            raise ValueError(f"Node ID {node_id} already in use.")

        self.nodes[node_id] = ChordNode(node_id, self.m)

        if len(self) == 1:
            logging.info(f"Node {node_id} joined the ring as the first node.")
        else:
            self.nodes[node_id].join(self.nodes_in_order[0])
            logging.info(f"Node {node_id} joined the ring.")

        return self.nodes[node_id]

    def leave(self, node_id: int) -> None:
        """
        Removes a Chord node from the Chord ring.
        :param node_id: The ID of the node to leave the ring.
        """
        if node_id not in self.nodes:
            raise ValueError("Node ID not in the ring.")

        self.nodes.pop(node_id).leave()

        logging.info(f"Node {node_id} left the ring.")

    def insert(self, key: str, value: object) -> None:
        """
        Inserts a key-value pair into the Chord ring.
        :param key: The key to insert.
        :param value: The value to store with the key.
        :raises ValueError: If the ring is empty.
        """
        if not self.nodes:
            raise ValueError("Cannot insert into an empty Chord ring.")

        self.nodes_in_order[0].insert(key, value)

        logging.info(f"Inserted key {key} with value {value}.")

    def lookup(self, key: str) -> list[object]:
        """
        Looks up a key in the Chord ring.
        :param key: The key to lookup.
        :return: The data stored with the key, or None if the key is not found.
        :raises ValueError: If the ring is empty.
        """
        if not self.nodes:
            raise ValueError("Cannot lookup in an empty Chord ring.")

        data = self.nodes_in_order[0].lookup(key)

        logging.info(f"Lookup key {key} returned value {data}.")

        return data
