import csv
from pwn import *
import random
import os

class Csv:
    def __init__(self, filename):
        self.filename = filename

        data = Csv.parse(filename)
        self.items = data
        self.cols = len(data)
        self.rows = len(data[0])

    @staticmethod
    def parse(file: str) -> list[str]:
        """Parses a csv file, returning a list of the parts that can be mutated"""
        with open(file) as f:
            data = list(csv.reader(f))

        return data
    
    @staticmethod
    def encode(cols: int, parts: list[list[str]]) -> str:
        """Encodes a list of mutated parts back into a string in a csv format"""

        lines = []
        for row in parts:
            lines.append(','.join(map(str, row[:cols])))

        return '\n'.join(lines)


def _append(item: list):
    # pick a random index
    idx = random.randrange(len(item))

    # generate a random string
    fuzz = ''.join(random.choices(string.ascii_uppercase + string.digits, k=990))

    # append
    item[idx][3] = item[idx][3] + fuzz

    return item
    

def extend(item: list):
    n = random.randrange(10, 30)
    return item * n

if __name__ == "__main__":
    # csv_file = Csv("./csv1.txt")
    items = Csv.parse("./csv1.txt")

    items = _append(items)
    items = extend(items)

    payload = Csv.encode(4, items)

    p = process("./csv1")
    p.sendline(payload)
    p.interactive()

