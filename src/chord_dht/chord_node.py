import hashlib


class ChordNode:
    """
    A node in a Chord-DHT ring.
    :cvar nid: The ID of the node.
    :cvar m: The number of bits in the hash space of the Chord ring.
    :cvar prev: The previous node in the ring.
    :cvar fingers: The finger table of the node.
    :cvar data: The key-value pairs stored in the node.
    """
    nid: int
    m: int
    next: 'ChordNode'
    prev: 'ChordNode'
    fingers: list['ChordNode']
    data: dict[str, object]

    def __init__(self, nid: int, m: int):
        """
        A node in a Chord-DHT ring.
        :param nid: The ID of the node.
        :param m: The number of bits in the ID hash space of the Chord ring.
        """
        self.nid = nid
        self.m = m
        self.next = self
        self.prev = self
        self.fingers = [self] * m
        self.data = {}

    def __str__(self) -> str:
        """
        A string representation of the Chord node.
        :return: A string representation of the Chord node.
        """
        return f"{self.nid}: Fingers: {[finger.nid for finger in self.fingers]} Next: {self.next.nid} Prev: {self.prev.nid}"

    def join(self, node: 'ChordNode' or None):
        """
        Joins a node to the Chord ring.
        :param node: The node to use as a starting point for joining the ring. If ``None``, the node joins as the first
        node in the ring.
        """
        if node:
            self.init_fingers(node)

            self.next = self.fingers[0]
            self.prev = self.next.prev

            self.update_others()

    def insert(self, key: str, value: object):
        """
        Inserts a key-value pair into the Chord ring.
        :param key: The key to insert.
        :param value: The value to store with the key.
        """
        node_id = self.hash_id(key)
        successor = self.successor(node_id)
        successor.data[key] = value

    def lookup(self, key: str) -> object or None:
        """
        Looks up a key in the Chord ring.
        :param key: The key to lookup.
        :return: The value associated with the key, or None if the key is not found.
        """
        node_id = self.hash_id(key)
        successor = self.successor(node_id)
        return successor.data.get(key, None)

    def successor(self, nid: int) -> 'ChordNode':
        """
        Finds the successor node for a given ID.
        :param nid: The ID to find the successor for.
        :return: The successor node for the given ID.
        """
        return self if is_successor(nid, self) else self.next.successor(nid)

    def init_fingers(self, node: 'ChordNode'):
        """
        Initializes the finger table of the node.
        :param node: The node to use as a starting point for initializing the finger table.
        """
        for i in range(self.m):
            fid = (self.nid + 2 ** i) % (2 ** self.m)
            self.fingers[i] = node.successor(fid)

    def update_others(self):
        """
        Updates the finger tables of other nodes in the ring to reflect the new node.
        """
        node = self.next
        while node != self:
            node.update_fingers(self)
            node = node.next

    def hash_id(self, key: str) -> int:
        """
        Computes the node ID for a given key by hashing the key into the hash space.
        :param key: The key to hash.
        :return: The ID of the node responsible for the key.
        """
        key_hash = hashlib.sha1(key.encode())
        return int(key_hash.hexdigest(), 16) % (2 ** self.m)


def is_successor(nid: int, node: ChordNode) -> bool:
    """
    Determines if a node is the successor of a given ID.
    :param nid: The ID to check the successor for.
    :param node: The node to check if it is the successor.
    :return: True if the node is the successor, False otherwise.
    """
    if node.next is node:
        return True
    if node.nid <= node.next.nid:
        return node.nid < nid < node.next.nid
    else:
        return node.nid < nid or nid < node.next.nid
