import random
import os

def duplication_mutation(part):
    _part = part[:]
    dupe_count = random.randint(0, 999)
    _part = _part * dupe_count
    return _part

def additive(part: str) -> str:
    """
    Additive mutation. Adds an random number of bytes to the string, including non
    16 byte aligned values.
    """
    _part = part[:].encode()
    num_extra = random.randint(1, 999)
    _part = _part + os.urandom(num_extra)
    return _part

def bitflip_mutation(part: str, mutation_index: int) -> str:
    _part = part[:].encode()
    if mutation_index:
        byte_index = mutation_index // 8
        bit_index = mutation_index % 8
        _part[byte_index] =  _part[byte_index] ^  (1 << (7 - bit_index))
    else:
        num_changes = len(part) * 0.5
        for _ in range(num_changes):
            byte_index = random.randint(0, len(part) - 1)
            bit_index = random.randint(0, 7)
            _part[byte_index] = _part[byte_index] & (1 << (7 - bit_index))
    return _part.decode()

def byteflip_mutation(part: str, mutation_index: int = 0) -> str:
    """
    Applies a byte flip mutation to the string.
    PARAMS:
        - part. A string representing the targeted mutation object
        - mutation_index: the index of the string to change
    For now, this will convert the string into a byte object, but this is a point for consideration
    # TODO: this may cause errors as it is passed into a file. Sometimes
    """
    # make a shadow copy
    _part = bytearray(part[:].encode())
    if mutation_index:
        _part[mutation_index] = random.randint(0, 255)
    else:
        num_change = int(len(part) * 0.67)
        for _ in range(num_change):
            _part[random.randint(0, len(part) - 1)] =  random.randint(0, 255)
           
    return bytes(_part) #TODO: consider returning a byte object

def increment_mutation(part: str, mutation_index: int) -> str:

    return str(mutation_index)

mutation_strategies = [
    bitflip_mutation, 
    byteflip_mutation, 
    increment_mutation,
    additive
]

def mutate(parts: list[str], mutation_count: int) -> list[str]:
    """Mutates one of the strings in parts based on the current mutation_count
    Parameters:
        parts: list of strings
        mutation_count: the number of mutations I assume
    This function alternates between strategies."""
    # TODO: we will also presumably have to send them 50 items at a time for multiprocessing
    # TODO: possibly change to byte object being passed in. 

    # Shallow clone parts list
    mutated_parts = parts[:] 
    part_i = mutation_count % len(parts)
    part_mutation_count = mutation_count // len(parts)

    mutation_strategy_index = part_mutation_count % len(mutation_strategies)
    mutation_strategy_count = part_mutation_count // len(mutation_strategies)
    
    mutation_strategy = mutation_strategies[mutation_strategy_index]

    mutated_parts[part_i] = mutation_strategy(parts[part_i], mutation_strategy_count)
    # print(mutation_count, p)

    return mutated_parts

# for testing purposes only
for i in range(100):
    res = duplication_mutation(b"hello\n")
    print(res.decode())
    print(len(res))
    

