import random
import string

def bitflip_mutation(part: str, mutation_index: int) -> str:
    return "TODO"

def increment_mutation(part: str, mutation_index: int) -> str:
    return str(mutation_index)

def fmtstring_mutation(part: str, mutation_index: int) -> str:
    random.seed(mutation_index)
    
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
        
    #print("Sending input:", part)
    return part
    
def additive_mutation(part: str, mutation_index: int) -> str:
    """
    Function that adds some fun amounts of bytes
    """
    random_bytes = ''.join(random.choices(string.digits, k=random.randint(0, 999)))
    m = part[:mutation_index] + random_bytes + part[mutation_index + 1:]
    return m

mutation_strategies = [bitflip_mutation, increment_mutation, fmtstring_mutation, additive_mutation]

def mutate(parts: list[str], mutation_count: int) -> list[str]:
    """Mutates one of the strings in parts based on the current mutation_count
    
    This function alternates between strategies."""
    # TODO: we will also presumably have to send them 50 items at a time for multiprocessing

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



