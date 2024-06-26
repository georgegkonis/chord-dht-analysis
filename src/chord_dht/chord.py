from src.chord_dht.chord_node import ChordNode


class Chord:
    m: int
    nodes_dict: dict[int, ChordNode]
    nodes_list: list[ChordNode]

    def __init__(self, m: int):
        """
        A Chord-DHT ring.
        :param m: The number of bits in the hash space.
        """
        self.m = m
        self.nodes_dict = {}
        self.nodes_list = []

    def __len__(self):
        return len(self.nodes_dict)

    def node_join(self, node_id: int) -> ChordNode:
        """
        Creates a new Chord node and joins it to the Chord ring.
        :param node_id: The ID of the new node.
        :return: The new Chord node.
        """
        if node_id < 0 or node_id >= 2 ** self.m:
            raise ValueError("Node ID out of bounds.")

        if node_id in self.nodes_dict.keys():
            raise ValueError("Node ID already in use.")

        print(f"Node {node_id} joining the ring.")

        node = ChordNode(node_id, self.m)

        # If the ring is empty, the new node is the only node in the ring.
        if len(self) == 0:
            node.join(None)
            self.nodes_dict[node_id] = node
            self.nodes_list.append(node)
            print(f"Node {node_id} is the first node in the ring.")

        # Otherwise, the new node joins the ring through the smallest existing node.
        else:
            smallest_node = self.nodes_list[0]
            node.join(smallest_node)
            self.nodes_dict[node_id] = node
            self.nodes_list.append(node)
            self.nodes_list.sort(key=lambda n: n.node_id)
            print(f"Node {node_id} joined through node {smallest_node.node_id}.")

        return node

    def node_leave(self, node_id: int):
        """
        Removes a Chord node from the Chord ring.
        :param node_id: The ID of the node to remove.
        """
        raise NotImplementedError("Not yet implemented.")

    def insert(self, key: str, value: object):
        """
        Inserts a key-value pair into the Chord ring.
        :param key: The key to insert.
        :param value: The value to store with the key.
        """
        if not self.nodes_dict:
            raise ValueError("No nodes in the Chord ring.")

        node = self.nodes_dict[0]
        node.insert(key, value)

    def lookup(self, key: str) -> object or None:
        """
        Looks up a key in the Chord ring.
        :param key: The key to lookup.
        :return: The value associated with the key, or None if the key is not found.
        """
        if not self.nodes_dict:
            raise ValueError("No nodes in the Chord ring.")

        node = self.nodes_dict[0]
        return node.lookup(key)
