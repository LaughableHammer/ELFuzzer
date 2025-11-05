from pwn import *
import random

def extend(item):
    num_times = random.randint(0, 100)
    try:
        item = item * num_times
        return bytearray(item)
    except:
        return item
    
"""
Function that adds some fun amounts of bytes
"""
def additive(item):
    if len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    random_bytes = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(0, 999)))
    item[idx:idx] = random_bytes.encode()
    return item

input_file = "./csv1.txt"
corpus = []
strats = [
    additive, 
    extend,
    extend
]
with open(input_file, 'rb') as file:
    all_bytes = bytearray(file.read())
    corpus.append(all_bytes)

    for _ in range(10000):
        strategy = random.choice(strats)
        mutate_target = random.choice(corpus)[:]
        res = strategy(mutate_target)

        corpus.append(res)

        if len(corpus) > 10:
            # del corpus[1:len(corpus)//2]  
            corpus = corpus[:len(corpus)//2]
            corpus.insert(0, all_bytes)

        p = subprocess.run(["./csv1"],
            input=res    
        )
        print("rc", p.returncode)