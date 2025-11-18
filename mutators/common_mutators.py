import random
import string
import struct

def extend(item: bytearray) -> bytearray:
    num_times = random.randint(0, 5)
    try:
        return item * num_times
    except:
        return item

def additive(item: bytearray) -> bytearray:
    """
    Function that adds some random amounts of ASCII characters at a random index
    """
    if len(item) > 10000 or len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    random_bytes = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 990)))
    item[idx:idx] = random_bytes.encode()
    return item

def bitflip_mutation(part: bytearray) -> bytearray:
    """
    Flips a random number of bits in random locations.
    """
    itr = max(10, int(len(part) * 0.3))
    data = part[:]
    for _ in range(itr):
        byte_idx = random.randrange(len(part))
        bit_idx = random.randrange(8)

        data[byte_idx] ^= 1 << bit_idx
    return data

def byteflip_mutation(part: bytearray) -> bytearray:
    """
    Does a byteflip (i.e flip 1 <-> 0)
    """
    itr = max(10, int(len(part) * 0.3))
    data = part[:]
    for _ in range(itr):
        byte_idx = random.randrange(len(part))
        data[byte_idx] ^= 0xFF
    return data

def fmtstring_mutation(part: bytearray) -> bytearray:
    data = part[:]
    if not part:
        index_to_modify = []
    else:
        # Select random indices to modify, quantity based on mutation_index
        # count = (mutation_index // 4) if mutation_index > 4 else 1
        count = max(1, min(count, len(part)))
        index_to_modify = random.sample(range(len(part)), k=count)
    
    for index in index_to_modify:
        fmt = f"%{random.randint(1, 6)}$n" # %n usually is more reliable to crash
        data = data[index:] + fmt + data[:index]
        
    return data

def known_ints(parts: bytearray) -> bytearray:
    """
    TODO: possibly move this to the common mutator
    Also should probably check that whatever its replacing its an integer (but it would be 
    difficult)
    """
    KNOWN_INTS = [
        -1, 0, 1, 
        16, 32, 64, 127, 128, 255,
        256, 512, 1024, 4096,
        0x7FFFFFFF, 0x80000000, 0xFFFFFFFF
    ]
    INT_BYTES = [struct.pack("<I", i & 0xFFFFFFFF) for i in KNOWN_INTS] # seems a little complex

    data = parts[:]

    for i in range(0, len(data) - 3, 4):
        if random.random() < 0.1:
            data[i:i+4] = random.choice(INT_BYTES)

    return data

def mutate(part: bytearray):
    strategies = [
        extend,
        additive,
        bitflip_mutation,
        byteflip_mutation,
        fmtstring_mutation,
        known_ints
    ]
    chosen_strategy = random.choice(strategies)
    return chosen_strategy(part)