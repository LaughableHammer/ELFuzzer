import csv
# I'm very happy to rearchitect the design, I just 
# don't want us to hardcode from the start

# Maybe classes would be helpful if we have more methods / internal data
# Python classes 💔 

# If possible it would be nice for us to use the strategy design pattern
# and be able to swap out the functions verbatism

# TODO: refactor this class's api, I just want a prototype
# Please don't create other classes based on this one until its refactered
class Plaintext:
    def __init__(self, file: str):
        self.file = file

    def parse(self) -> list[str]:
        return [self.file]

    def encode(self, parts: list[str]) -> str:
        return parts[0]

# Temporary measure for now, can make it non-static later but this makes sense, changes should be quick
# so just let me know
class Csv:
    @staticmethod
    def parse(file: str) -> list[str]:
        """Parses a csv file given a file name, returns a list of parts to be mutated"""
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
