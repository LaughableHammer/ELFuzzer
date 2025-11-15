import random
from .common_mutators import extend, additive
import globalVar

def json_csv_mutate(parts: list[str], mutation_count: int) -> list[str]:
    """
    This function takes in the file contents of the example input file and the 
    binary path. The function will then generate inputs and return them
    """        
    csv_json_strategies = [additive, extend]

    if isinstance(parts, list):
        joined = "\n".join(parts)
    else:
        joined = str(parts)

    all_bytes = bytearray(joined.encode())

    if not globalVar.corpus:
        globalVar.corpus = []
        globalVar.corpus.append(all_bytes)

    src = random.choice(globalVar.corpus)
    mutate_target = bytearray(src)

    strategy = random.choice(csv_json_strategies)
    res = strategy(mutate_target)

    if len(res) > 150000:
        res = res[:150000]

    globalVar.corpus.append(bytearray(res))
    
    if len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:] # keep half
        globalVar.corpus.insert(0, bytearray(all_bytes))
    globalVar.corpus = [c for c in globalVar.corpus if len(c) <= 150000]

    # Return as list of strings (decoded lines)
    try:
        decoded = res.decode('latin1').splitlines(keepends=True)
    except Exception:
        decoded = [joined]
    return decoded
