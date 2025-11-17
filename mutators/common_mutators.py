import random
import string

def util_gen_random_str(len = 999):
    return ''.join(random.choices(string.ascii_uppercase, k=len))

def primitive_mutate(item: bytearray) -> bytearray:
    strategies = [
        extend,
        additive,
        bad_bytes
    ]
    strat = random.choice(strategies)
    return strat(item)

def extend(item: bytearray) -> bytearray:
    num_times = random.randint(0, 5)
    try:
        return item * num_times
    except:
        return item

"""
Function that adds some fun amounts of bytes at a random index
"""
def additive(item: bytearray) -> bytearray:
    if len(item) > 10000 or len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    random_bytes = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 9900)))
    item[idx:idx] = random_bytes.encode()
    return item

def bad_bytes(item: bytearray) -> bytearray:
    """
    Function that adds bad bytes, such as %n, in the middle of the 
    byte string.

    For now, this is just a format string with %n, which seems to break easily
    """
    idx = random.randint(0, max(1, len(item) - 1))
    # item.insert(idx, b"%n")
    for b in b"%n":
        item.insert(idx, b)
        idx += 1
    return item
    

