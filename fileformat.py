import csv
import itertools
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
    def __init__(self, raw_content: str):
        self.raw_content = raw_content
        
        # split() is sus, if any alternative to parse file contents lmk
        self.data = list(csv.reader(self.raw_content.split()))
        self.cols = len(self.data[0])
        self.rows = len(self.data)
    
    def parse(self) -> list[str]:
        """Parses a csv file, returning a list of the parts that can be mutated"""
        return [s for row in self.data for s in row]
        
    def encode(self, parts: list[str]) -> str:
        """Encodes a list of mutated parts back into a string in a csv format"""
        lines = [parts[i:i + self.cols] for i in range(0, len(parts), self.cols)]
        lines = map(lambda x : ','.join(x), lines)  
        csv = '\n'.join(lines)
        return csv
