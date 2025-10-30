from pwn import *
import random

def extend(item):
    num_times = random.randint(0, 100)
    try:
        items = item * num_times
        return bytearray(item)
    except MemoryError:
        return item
    
"""
Function that adds some fun amounts of bytes
"""
def additive(item):
    if len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    # idx=14
    # random_bytes = os.urandom(random.randint(900, 999)) <-- this might cause null bytes to be written
    random_bytes = ''.join(random.choices(string.digits, k=random.randint(0, 999)))
    item[idx:idx] = random_bytes.encode()
    # for _ in range(15):
    return item

input_file = "./json1.txt"
corpus = []
strats = [
    additive
]
with open(input_file, 'rb') as file:
    all_bytes = bytearray(file.read())
    corpus.append(all_bytes)

    # 100 iterations
    for _ in range(1000000):
        strategy = random.choice(strats)
        mutate_target = random.choice(corpus)[:]
        print(mutate_target)
        res = strategy(mutate_target)
        # res = mutate_target
        print(res.decode())
        # continue

        # corpus.append(res)
        p = subprocess.run(["./json1"],
            input=res
        )
        print("rc", p.returncode)

