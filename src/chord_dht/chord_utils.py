import hashlib


def hash_id(key: str, m: int) -> int:
    """
    Hashes a key to an ID in the Chord ring.
    :param key: The key to hash.
    :param m: The number of bits in the hash space.
    :return: The hashed ID of the key.
    """
    key = key.encode()
    key = hashlib.sha1(key)
    key = key.hexdigest()

    return int(key, 16) % (2 ** m)


def in_open_range(start: int, end: int, target_id: int) -> bool:
    """
    Determines if the target ID is in an open range.
    :param start: The start of the range.
    :param end: The end of the range.
    :param target_id: The ID to check.
    :return: ``True`` if the target ID is in the range, ``False`` otherwise.
    """
    if start < end:
        return start < target_id < end
    else:
        return target_id > start or target_id < end


def in_right_closed_range(start: int, end: int, target_id: int) -> bool:
    """
    Determines if the target ID is in a right-closed range.
    :param start: The start of the range.
    :param end: The end of the range.
    :param target_id: The ID to check.
    :return: ``True`` if the target ID is in the range, ``False`` otherwise.
    """
    if start < end:
        return start < target_id <= end
    else:
        return target_id > start or target_id <= end
