from pwn import *
import random

"""
For now, we need to solve csv1 by being 
completely random

"""
def extend(item):
    num_times = random.randint(0, 100)
    item = item * num_times
    return bytearray(item)
    
"""
Function that adds some fun amounts of bytes
"""
def additive(item):
    if len(item) < 2:
        return item
    idx = random.randint(0, len(item) - 1)
    # random_bytes = os.urandom(random.randint(900, 999)) <-- this might cause null bytes to be written, crashing the program
    random_bytes = ''.join(random.choices(string.ascii_uppercase + string.digits, k=990))
    item[idx:idx] = random_bytes.encode()
    # for _ in range(15):
    return item


from pwn import *
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

    # 100 iterations
    for _ in range(1000):
        strategy = random.choice(strats)
        mutate_target = random.choice(corpus)[:]
        # print(mutate_target)
        res = strategy(mutate_target)

        corpus.append(res)
        p = subprocess.run(["./csv1"],
            input=res    
        )
        print("rc", p.returncode)

