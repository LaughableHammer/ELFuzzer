import random
import globalVar
from .common_mutators import additive, extend
import string

# def mutate_cell(rows: list[list[str]]) -> list[list[str]]:
#     if not rows or len(rows) <= 1:
#         return rows

#     new_rows = [r[:] for r in rows]

#     # randomly mutate 1 cell (excluding header row)
#     cell_row = random.randint(1, len(new_rows) - 1)
#     cell_col = random.randint(0, len(new_rows[0]) - 1)

#     cell = new_rows[cell_row][cell_col]

#     if not cell:
#         return rows

#     cell_bytes = bytearray(cell, 'latin1', errors='ignore')

#     cell_bytes = additive(cell_bytes)
#     new_rows[cell_row][cell_col] = cell_bytes.decode('latin1', errors='ignore')

#     return new_rows

# csv_strategies = [mutate_cell]

class JpgSegment:
    def __init__(self, marker: bytes, data: bytes):
        self.marker = marker
        self.data = data

    def encode(self, size=None):
        if size == None:
            size = 2 + len(self.data)
        return self.marker + size.to_bytes(2, 'big') + self.data


def jpg_parse(file_content: bytes) -> list[JpgSegment]:
    segments = []
    i = 2

    # there is no chance the jpeg is spec compliant if its less than 6 bytes
    if (len(file_content) < 6):
        return []
    
    while i < len(file_content) - 2:
        marker = file_content[i:i+2]

        if marker == b'\xff\xda':
            data = file_content[i+2:len(file_content)-2]
            i = len(file_content)-2
        else:
            size = int.from_bytes(file_content[i:2:i+4], 'big')
            data = file_content[i+4:i+2+size+1]
            i = i+2+size+1
        
        segments.append(JpgSegment(marker, data))

    return segments

def jpg_mutate(file_content: bytes, seed: int) -> bytes:
    segments = jpg_parse(file_content)

    # cloning segments

    # plaintext mutation within segments

    # changing markers within segments

    # try encoding it with incorrect lengths

    

    encoded_jpg = b"\xff\xd8" + b''.join([segment.encode() for segment in segments]) + b"\xff\xd9"
    return encoded_jpg


def csv_mutate(rows: list[list[str]]) -> list[list[str]]:
    if not rows:
        return rows
    
    if not globalVar.corpus:
        globalVar.corpus.append(rows)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]

    src = random.choice(globalVar.corpus)
    mutated = [r.copy() for r in src]

    strategy = random.choice(csv_strategies)
    mutated = strategy(mutated)

    # occasionally duplicate some rows
    if mutated and random.random() < 0.1:
        row_to_dup = random.choice(rows)
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

    return mutated