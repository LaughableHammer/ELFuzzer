from mutators.common_mutators import mutate

def plaintext_mutate(parts: str) -> bytearray:
    """Mutates one of the strings in parts
    This function alternates between strategies."""
  
    mutated = parts[:].encode()
    mutated = mutate(bytearray(mutated))
    return mutated
