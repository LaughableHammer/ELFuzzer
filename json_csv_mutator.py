import string
import random

def extend(item: bytearray) -> bytearray:
    if len(item) > 10000:
        return item
    num_times = random.randint(0, 100)
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
    random_bytes = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1, 999)))
    item[idx:idx] = random_bytes.encode()
    return item

# Keep corpus persistent
corpus = []
csv_json_strategies = [additive, extend, extend]

def json_csv_mutate(parts: list[str], mutation_count: int) -> list[str]:
    """
    This function takes in the file contents of the example input file and the 
    binary path. The function will then generate inputs and return them
    """
    global corpus

    if isinstance(parts, list):
        joined = "\n".join(parts)
    else:
        joined = str(parts)

    all_bytes = bytearray(joined.encode())

    if not corpus:
        corpus.append(all_bytes)

    strategy = random.choice(csv_json_strategies)
    mutate_target = random.choice(corpus)[:]
    res = strategy(mutate_target)

    corpus.append(res)
    
    if len(corpus) > 10:
        corpus = corpus[:len(corpus)//2]
        corpus.insert(0, all_bytes)
    corpus = [c for c in corpus if len(c) <= 10000]

    # Return as list of strings (decoded lines)
    try:
        decoded = res.decode(errors='ignore').splitlines()
    except Exception:
        decoded = [joined]
    return decoded