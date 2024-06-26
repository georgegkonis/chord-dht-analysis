import hashlib


class ChordNode:
    node_id: int
    m: int
    next: 'ChordNode'
    prev: 'ChordNode' or None
    fingers: list['ChordNode']
    data: dict[str, object]

    def __init__(self, node_id: int, m: int):
        """
        A node in a Chord-DHT ring.
        :param node_id: The ID of the node.
        :param m: The number of bits in the hash space of the Chord ring.
        """
        self.node_id = node_id
        self.m = m
        self.next = self
        self.prev = None
        self.fingers = [self] * m
        self.data = {}

    # region Basic Operations

    def insert(self, key: str, value: object):
        """
        Inserts a key-value pair into the Chord ring.
        :param key: The key to insert.
        :param value: The value to store with the key.
        """
        node_id = self._compute_node_id(key)
        successor = self._find_successor(node_id)
        successor.data[key] = value

    def lookup(self, key: str) -> object or None:
        """
        Looks up a key in the Chord ring.
        :param key: The key to lookup.
        :return: The value associated with the key, or None if the key is not found.
        """
        node_id = self._compute_node_id(key)
        successor = self._find_successor(node_id)
        return successor.data.get(key, None)

    def join(self, node: 'ChordNode' or None):
        """
        Joins a node to the Chord ring.
        :param node:
        """
        if node:
            self._init_fingers(node)
            self._update_others()
        else:
            self.fingers = [self] * self.m
            self.prev = self

    # endregion

    def _find_successor(self, node_id: int) -> 'ChordNode':
        """
        Finds the successor node of a given node ID.
        :param node_id: The ID of the node to find the successor of.
        :return: The successor node of the given node ID.
        """
        if self.prev is None:
            return self
        elif self.node_id < node_id <= self.next.node_id:
            return self.next
        else:
            node = self.closest_preceding_node(node_id)
            return node._find_successor(node_id)

    def _find_predecessor(self, node_id: int) -> 'ChordNode':
        """
        Finds the predecessor node of a given node ID.
        :param node_id: The ID of the node to find the predecessor of.
        :return: The predecessor node of the given node ID.
        """
        node = self
        while not (node.node_id < node_id <= node.next.node_id):
            node = node.closest_preceding_node(node_id)
        return node

    def closest_preceding_node(self, key):
        """
        Finds the closest preceding node of a given key.
        :param key: The key to find the closest preceding node of.
        :return: The closest preceding node of the given key.
        """
        for i in range(self.m - 1, -1, -1):
            if self.node_id < self.fingers[i].node_id < key:
                return self.fingers[i]
        return self

    def _init_fingers(self, node: 'ChordNode'):
        """
        Initializes the finger table of the node by finding the successors of the node's keys.
        :param node: The node to initialize the finger table with.
        """
        self.fingers[0] = node._find_successor(self.node_id)

        self.prev = self.next.prev
        self.next.prev = self

        for i in range(self.m - 1):
            if self.node_id <= self.fingers[i].node_id < (self.node_id + 2 ** i) % (2 ** self.m):
                self.fingers[i + 1] = self.fingers[i]
            else:
                self.fingers[i + 1] = node._find_successor((self.node_id + 2 ** (i + 1)) % (2 ** self.m))

    def _update_others(self):
        for i in range(self.m):
            pred_id = (self.node_id - 2 ** i + 2 ** self.m) % (2 ** self.m)
            pred = self._find_predecessor(pred_id)
            pred.update_fingers(self, i)

    def update_fingers(self, s, i):
        if self.node_id <= s.node_id < self.fingers[i].node_id:
            self.fingers[i] = s
            pred = self.prev
            pred.update_fingers(s, i)

    def _compute_node_id(self, key: str) -> int:
        """
        Computes the node ID for a given key by hashing the key into the hash space.
        :param key: The key to hash.
        :return: The ID of the node responsible for the key.
        """
        key_hash = hashlib.sha1(key.encode())

        return int(key_hash.hexdigest(), 16) % (2 ** self.m)
