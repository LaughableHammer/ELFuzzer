from mutators.common_mutators import mutate

"""
TODO: consider whether we want strings or 
byte object to be passed in, as things may break when decoding 
byteobjects (even with errors=ignore)

This is pretty much a wrapper for common_mutator
"""

def plaintext_mutate(parts: str) -> str:
    """Mutates one of the strings in parts
    This function alternates between strategies."""
    # TODO: we will also presumably have to send them 50 items at a time for multiprocessing
   
    mutated = bytearray(parts[:])
    mutated = mutate(bytearray(mutated))
    return mutated.decode()



