import random
import string

def util_wrap_signed(value, width):
    """
    Helps wrap the integer from arithmatic mutation
    to fit into the width that it used to be to prevent overflowing.    
    """
    mask = ((1 << width * 8) - 1)
    truncated = value & mask
    sign_bit = 1 << (width * 8 - 1)
    return (truncated ^ sign_bit) - sign_bit

def arithematic_mutate(item: bytearray) -> bytearray:
    """
    Finds random bytes with predetermined lengths, then
    add/subtract from them
    """
    width = random.choice([1, 2, 4, 8])
    if len(item) < width:
        return item
    try:
        offset = random.randint(0, len(item) - width - 1)
    except ValueError:
        return item

    start_idx = offset
    end_idx = start_idx + width
    obtained_bytes = item[start_idx:end_idx]
    value = int.from_bytes(obtained_bytes, byteorder="little")

    if random.random() < 0.7:
        result = value + random.randint(-10, 10)
    else:
        result = value + random.randint(-100, 100)

    result = util_wrap_signed(result, width)
    
    item[start_idx:end_idx] = result.to_bytes(length=width, byteorder="little", signed=True)
    return item

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

def get_format_specifier() -> str:
    if random.random() < 0.1:
        return random.choice(["%10000$s", "%%s%%s"])
    else:
        return f"%{random.randint(1, 6)}$n" # %n usually is more reliable to crash

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
        data = data[index:] + get_format_specifier().encode() + data[:index]
        
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

def get_random_magic_num() -> int:
    magic_numbers = [b'-1', b'0xFF', b'0x00', b'0xFFFF', b'0x0000', b'0x80000000', b'0x40000000', b'0x7FFFFFFF', b'9999999999999999', b'-9999999999999999']
    return int(random.choice(magic_numbers), 16)

def mutate(part: bytearray, keep_length=False):
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
        arithematic_mutate
    ]

    chosen_strategy = random.choice(strategies)
    return chosen_strategy(part)
