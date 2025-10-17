# ============================================================================
#                           File format parser
# ============================================================================
# I'm very happy to rearchitect the design, I just 
# don't want us to hardcode from the start

# Maybe classes would be helpful if we have more methods / internal data

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

# Whoops I should've started working on plain text instead of diving straight into CSV...
# class Csv:
#     # TODO: refactor
#     cols = 4

#     def parse(self, file: str) -> list[str]:
#         """Parses a csv file, returning a list of the parts that can be mutated"""
#         lines = file.split("\n")
        
#         parts = []
#         for line in lines:
#             # TODO: refactor to use proper csv library as commas may be contained inside strings
#             parts += line.split(",")

#         return parts


#     def encode(self, parts: list[str]) -> str:
#         """Encodes a list of mutated parts back into a string in a csv format"""

#         lines = []
#         for i in range(0, len(parts), self.cols):
#             lines.append(','.join(parts[i:i+self.cols]))

#         return '\n'.join(lines)
