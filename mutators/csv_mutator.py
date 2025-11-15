import random
import globalVar
from .common_mutators import additive, extend
from io import StringIO # allows dealing with file-like objects in memory
import csv

def rows_to_csv(rows: list[list[str]]) -> str:
    f = StringIO()
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)
    return f.getvalue()

def mutate_cell(rows: list[list[str]]) -> list[list[str]]:
    if not rows or len(rows) <= 1:
        return rows

    new_rows = [r[:] for r in rows]

    # randomly mutate 1 cell (excluding header row)
    cell_row = random.randint(1, len(new_rows) - 1)
    cell_col = random.randint(0, len(new_rows[0]) - 1)

    cell = new_rows[cell_row][cell_col]

    if not cell:
        return rows

    cell_bytes = bytearray(cell, 'latin1', errors='ignore')

    cell_bytes = additive(cell_bytes)
    new_rows[cell_row][cell_col] = cell_bytes.decode('latin1', errors='ignore')

    return new_rows

csv_strategies = [mutate_cell]

# def csv_mutate(rows: list[list[str]]) -> list[list[str]]:  
def csv_mutate():
    # if not rows:
    #     return rows
    
    # if not globalVar.corpus:
    #     globalVar.corpus.append(rows)
    # elif len(globalVar.corpus) > 20:
    #     globalVar.corpus = globalVar.corpus[10:]

    src = random.choice(globalVar.corpus)
    mutated = [r.copy() for r in src]

    strategy = random.choice(csv_strategies)
    mutated = strategy(mutated)

    # occasionally duplicate some rows
    if mutated and random.random() < 0.1:
        row_to_dup = random.choice(src)
        num_dups = random.randint(1, 5)
        for _ in range(num_dups):
            mutated.insert(random.randint(1, len(mutated)), row_to_dup.copy())

    if len(mutated) > 150000:
        mutated = mutated[:150000]

    if random.random() < 0.1:
        globalVar.corpus.insert(0, mutated)
    else:
        globalVar.corpus.append(mutated)

    #print(f"[DEBUG] rows={len(mutated)}, total_cells={sum(len(r) for r in mutated)}, avg_cell_len={sum(len(c) for r in mutated for c in r) / max(1, sum(len(r) for r in mutated)):.2f}")
   
    # mutate
    # convert to str
    mutated_csv_text = rows_to_csv(mutated)
    return mutated_csv_text