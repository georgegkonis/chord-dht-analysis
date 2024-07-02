from IPython.core.display_functions import display

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
        return sorted(self.nodes.values(), key=lambda n: n.nid)

    def node_join(self, nid: int) -> None:
        """
        Creates a new Chord node and joins it to the Chord ring.
        :param nid: The ID of the node to join the ring.
        :raises ValueError: If the node ID is out of bounds or already in use.
        """
        if nid < 0 or nid >= 2 ** self.m:
            raise ValueError("Node ID out of bounds.")

        if nid in self.nodes:
            raise ValueError("Node ID already in use.")

        node = ChordNode(nid, self.m)

        # If the ring is empty, the new node is the only node in the ring.
        if len(self) == 0:
            node.join(None)
            self.nodes[nid] = node
            print(f"Node {nid} is the first node in the ring.")

        # Otherwise, the new node joins the ring through the first existing node.
        else:
            first_node = self.nodes_in_order[0]
            node.join(self.nodes_in_order[0])
            self.nodes[nid] = node
            print(f"Node {nid} joined through node {first_node.nid}.")

    def node_leave(self, node_id: int) -> None:
        """
        Removes a Chord node from the Chord ring.
        :param node_id: The ID of the node to leave the ring.
        """
        raise NotImplementedError("Not yet implemented.")

    def insert(self, key: str, value: object) -> None:
        """
        Inserts a key-value pair into the Chord ring.
        :param key: The key to insert.
        :param value: The value to store with the key.
        :raises ValueError: If the ring is empty.
        """
        if not self.nodes:
            raise ValueError("No nodes in the Chord ring.")

        node = self.nodes[0]
        node.insert(key, value)

    def lookup(self, key: str) -> object or None:
        """
        Looks up a key in the Chord ring.
        :param key: The key to lookup.
        :return: The value associated with the key, or ``None`` if the key cannot be found.
        :raises ValueError: If the ring is empty.
        """
        if not self.nodes:
            raise ValueError("No nodes in the Chord ring.")

        return self.nodes[0].lookup(key)


if __name__ == "__main__":

    data = {
        "Stanford": {"name": "Zuckerberg", "awards": 2},
        "MIT": {"name": "Gates", "awards": 3},
        "Harvard": {"name": "Buffett", "awards": 1},
        "Princeton": {"name": "Bezos", "awards": 4},
        "Yale": {"name": "Clinton", "awards": 1},
        "Columbia": {"name": "Obama", "awards": 2},
        "Chicago": {"name": "Bernanke", "awards": 1},
        "Caltech": {"name": "Feynman", "awards": 3},
        "Penn": {"name": "Trump", "awards": 0}
    }

    m = 2
    chord = Chord(m)

    for i in range(2 ** m):
        chord.node_join(i)

    print('\n', chord)
