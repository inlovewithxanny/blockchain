import hashlib
from binascii import hexlify


def get_hash(string: str, /):
    return hexlify(hashlib.sha256(string.encode("utf-8")).digest()).decode("utf-8")


def get_zero_hash(string: str, /):
    hash = get_hash(string)

    while hash[:3] != "000":
        hash = get_hash(hash)

    return hash


def is_even(num: int):
    return num % 2 == 0


def get_merkle_root(hash_list: list[str]):
    if len(hash_list) == 0:
        return None
    elif len(hash_list) == 1:
        return hash_list[0]

    new_hash_list = []

    if len(hash_list) % 2 != 0:
        hash_list.append(hash_list[-1])

    for i in range(0, len(hash_list), 2):
        combined_hash = hash_list[i] + hash_list[i + 1]
        new_hash = get_zero_hash(combined_hash)
        new_hash_list.append(new_hash)

    return get_merkle_root(new_hash_list)
