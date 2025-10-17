def bitflip_mutation(part: str, mutation_index: int) -> str:
    return "TODO"

def increment_mutation(part: str, mutation_index: int) -> str:
    return str(mutation_index)

mutation_strategies = [bitflip_mutation, increment_mutation]

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



