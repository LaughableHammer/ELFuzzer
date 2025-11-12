import random
import string

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
    random_bytes = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 990)))
    item[idx:idx] = random_bytes.encode()
    return item