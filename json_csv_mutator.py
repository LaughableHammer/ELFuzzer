import string
import random

def extend(item: bytearray) -> bytearray:
    num_times = random.randint(0, 5)
    try:
        return item * num_times
    except:
        return item
    
"""
Function that adds some fun amounts of bytes at a random index
"""
def additive(item: bytearray) -> bytearray:
    if len(item) > 100000 or len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    random_bytes = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1, 900)))
    item[idx:idx] = random_bytes.encode()
    return item

# Keep corpus persistent
corpus = []
csv_json_strategies = [additive, extend]

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
        
    src = random.choice(corpus)
    mutate_target = bytearray(src)

    strategy = random.choice(csv_json_strategies)
    res = strategy(mutate_target)

    if len(res) > 150000:
        res = res[:150000]

    corpus.append(bytearray(res))
    
    if len(corpus) > 20:
        corpus = corpus[10:] # keep half
        corpus.insert(0, bytearray(all_bytes))
    corpus = [c for c in corpus if len(c) <= 150000]

    # Return as list of strings (decoded lines)
    try:
        decoded = res.decode('latin1').splitlines(keepends=True)
    except Exception:
        decoded = [joined]
    return decoded
