import random
import string

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
    idx = random.randint(0, len(item))
    if random.random() < 0.01:
        random_bytes = ''.join(random.choices(string.ascii_uppercase, k=random.randint(500, 999)))
    else:
        random_bytes = f'{random.randint(-999999, 999999)}'
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
        count = max(1, min(0, len(part)))
        index_to_modify = random.sample(range(len(part)), k=count)
    
    for index in index_to_modify:
        fmt = f"%{random.randint(1, 6)}$n" # %n usually is more reliable to crash
        data = data[index:] + fmt.encode() + data[:index]
        
    return data

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

def mutate(part: bytearray) -> bytearray:
    strategies = [
        extend,
        additive,
        additive,
        additive,
        additive, # higher chance for BOF
        bitflip_mutation,
        byteflip_mutation,
        random_char,
        fmtstring_mutation,
    ]
    chosen_strategy = random.choice(strategies)
    return chosen_strategy(part)
