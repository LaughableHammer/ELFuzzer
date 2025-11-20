import random

# Adapted from https://h0mbre.github.io/Fuzzing-Like-A-Caveman/
def bitflip_mutation(part: str, mutation_index: int) -> str:
    """ Mutation index will determine how many bits will be flipped"""
    bytearr = bytearray(part, 'utf-8')
    
    # Flip at most 10% of bits of the input
    bits_to_flip = int((len(bytearr)) * (mutation_index % 10) * 0.01)
    
    indices = []

    # iterate selecting indexes until we've hit our num_of_flips number
    i = 0
    while i < bits_to_flip:
        indices.append(random.randint(0, len(bytearr) - 1))
        i += 1
    
    for i in indices:
        current = bytearr[i]
        current = (bin(current).replace("0b",""))
        current = "0" * (8 - len(current)) + current # pad to 8
        print("Old value:", current)
        
        flip = random.randint(0, 7)
        
        new_number = []
        for x in current:
            new_number.append(x)
            
            
        if new_number[flip] == "1":
            new_number[flip] = "0"
        else:
            new_number[flip] = "1"
   
        # change back into 1 string
        current = ''
        for x in new_number:
            current += x

        print("New value:", current)
        
        # convert to binary int
        current = int(current, 2)
        
        bytearr[i] = current
        

    return bytearr.decode("utf-8", errors="replace")

def increment_mutation(part: str, mutation_index: int) -> str:
    return str(mutation_index)

def fmtstring_mutation(part: str, mutation_index: int) -> str:
    if not part:
        index_to_modify = []
    else:
        # Select random indices to modify, quantity based on mutation_index
        count = (mutation_index // 4) if mutation_index > 4 else 1
        count = max(1, min(count, len(part)))
        index_to_modify = random.sample(range(len(part)), k=count)
    
    for index in index_to_modify:
        fmt = f"%{mutation_index}$s"
        part = part[index:] + fmt + part[:index]
        
    return part

plaintext_strategies = [bitflip_mutation, increment_mutation, fmtstring_mutation]

def plaintext_mutate(parts: list[str], mutation_count: int) -> str:
    """Mutates one of the strings in parts based on the current mutation_count
    
    This function alternates between strategies."""
    # TODO: we will also presumably have to send them 50 items at a time for multiprocessing

    # Shallow clone parts list
    mutated_parts = parts[:] 
    part_i = mutation_count % len(parts)
    part_mutation_count = mutation_count // len(parts)

    mutation_strategy_index = part_mutation_count % len(plaintext_strategies)
    mutation_strategy_count = part_mutation_count // len(plaintext_strategies)
    
    mutation_strategy = plaintext_strategies[mutation_strategy_index]

    mutated_parts[part_i] = mutation_strategy(parts[part_i], mutation_strategy_count)
    # print(mutation_count, p)

    return ''.join(mutated_parts)



