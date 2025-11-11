import csv
import random
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
    
    def fileFormat(self) -> str:
        return 'txt'

# Temporary measure for now, can make it non-static later but this makes sense, changes should be quick
# so just let me know
class Csv:
    
    # @staticmethod
    def parse(file: str) -> list[str]:
        """Parses a csv file given a file name, returns a list of parts to be mutated"""
        with open(file) as f:
            data = list(csv.reader(f))
        self.array = data
        return data
    
    @staticmethod
    def encode(cols: int, parts: list[list[str]]) -> str:
        """Encodes a list of mutated parts back into a string in a csv format"""

        lines = []
        for row in parts:
            lines.append(','.join(map(str, row[:cols])))

        return '\n'.join(lines)
    
    def __init__(self, file: str) -> list[str]:
        """
        Initiates a CSV class object, with the parsed format in itself. 
        """
        with open(file) as f:
            data = list(csv.reader(f))
        self.array = data

        # todo: error check
        self.row = len(data)
        self.col = len(data[0])
        return data

    @staticmethod
    def mutate_duplicate_row(obj):
        # STUB
        return
    
    @staticmethod
    def mutation_byte_flip(obj):
        pass

    @staticmethod
    def mutation_bit_flip(obj):
        pass

    @staticmethod
    def mutation_expand_value(obj):
        pass

    @staticmethod
    # Not too sure if this is cool
    def mutation_add_column(obj):
        pass

    @staticmethod
    # similar to duplicate row, but it just adds an entirely random row
    def mutation_add_row(obj):
        pass

    """
    Considerations: make the mutation function belonging to each instance
    so that it is cleaner to call. 
    """
    def mutate():
        strategies = [
            Csv.mutate_duplicate_row
        ]
        chosen = random.choice(strategies)
        chosen.mutate(self)

        """
        Pick various strategies
        """

