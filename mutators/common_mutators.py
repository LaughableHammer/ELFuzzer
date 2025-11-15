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

# Gynvael’s Magic Numbers (https://h0mbre.github.io/Fuzzing-Like-A-Caveman/)
def random_char(item: bytearray) -> bytearray:
    magic_numbers = [b'%s', b'-1', b'0xFF', b'0x00', b'0xFFFF', b'0x0000', b'0x80000000', b'0x40000000', b'0x7FFFFFFF']
    value = random.choice(magic_numbers)

    if not item or len(item) < len(value):
        return bytearray(value)
    
    mode = random.choice(['replace', 'insert', 'splice'])

    match mode:
        case 'replace':
            return bytearray(value)
        case 'insert':
            idx = random.randint(0, len(item) - 1)
            return item[:idx] + bytearray(item) + item[idx:]
        case 'splice':
            start = random.randint(0, len(item) - len(value))
            end = start + len(value)
            return item[:start] + value + item[end:]