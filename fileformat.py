import csv
import json
import random
import math
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

class Json:
    """
    File format representing a JSON file.    
    """
    def __init__(self, file:str):
        """
        Parse the provided file.
        Possible structures:
            - Dictionary format
            - Array of tuples (arr representing path, val) <-- Not the worst, but have to find a way to parse it back, and easier to run mutations on
            - Flatten into string, and use string manipulation to find specific components and change that. Would be a bit cursed, given that there may be lists in json object, but I suppose that can still be done. 
        TODO: think of more mutations
        """
        with(file, "r") as f:
            self._format = json.loads(f.read())

    @staticmethod
    def _flatten(data, parent_key='', sep='.'):
        items = []
        for key, value in data.items():
            new_key = parent_key + key if not parent_key else parent_key + sep + key
            if isinstance(value, dict):
                items.extend(Json._flatten(value, new_key, sep=sep))
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    list_key = f'{new_key}{sep}{idx}'
                    if isinstance(item, dict):
                        items.extend(Json._flatten(item, list_key, sep=sep))
                    else:
                        items.append((list_key, item))
            else:
                items.append((new_key, value))
        return items
    
    def encode(self) -> bytearray:
        """
        Turns the parsed format into JSON string object again

        TODO: figure out what the hell is going on here
        Possibly use a flatdict library that creates a flattened dictionary
        """
        root = {}
        for path, value in self._format:
            current = root
            path = path.split(".") # delimit, using "." TODO: could instead store using an array???
            for idx, key in enumerate(path):
                is_last = (idx == len(path) - 1)
                if isLast:
                    # final key
                    if (isinstance(key, int)):
                        while len(current) < key:
                            current.append(None)
                    else:
                        current[key] = value
                    continue
                else:
                    # since it isn;t last, we check what comes next
                    next = path[i+1]
                    # descend
                    # if its an integer i.e. in an array    
                    """
                    Check ahead and add appropriate containers
                    """
                    if isinstance(next, int):
                        # found an integer, therefore it should be an array
                        while len(current) <= key:
                            current
                    current = current[key]
                return
                    
        
        return json.dumps(root)




    def mutate(self):
        """
        Takes itself and calls one of the mutate functions
        """
        pass

    def _mutate_duplicate(self):
        """
        Duplicates some entry somewhere to a random location.
        Takes two choices from the tuple, one to get a random path, the other a value, and then add that to the array. 
        """
        itr = len(self._format) * 0.3
        for _ in range(itr):
            path, _ = random.choice(self._format)
            _, value = random.choice(self._format)
            self._format.append((path, value))

    def _mutate_change_entry(self):
        """
        Picks a few random entry
        """
        itr = len(self._format) * 0.3
        for _ in range(itr):
            idx = math.floor(random.randint(0, len(self._format) - 1 )) # pick a random index
            path = self._format[idx]
            # ideas: either conform to the type or dont. For now I will not conform
            if isinstance(value, list):
                value = value * random.randint(0, 20)
            else:
                value = random.randbytes(random.randint(1, 500))
            self._format[idx] = (path, value)

    def _mutate_add_depth(self):
        """
        Adds more depth, using random generated keys (or duplicate)
        """
    pass
            
    
    def _mutate_remove_entries(self):
        """
        remove items entirely
        """
        itr = len(self._format) * 0.3
        for _ in range(itr):
            idx = math.floor(random.randint(0, len(self._format) - 1 )) # pick a random index
            self._format.pop(idx)

    def _mutate_set_null(self):
        """
        Makes certain entries blank
        """
        itr = len(self._format) * 0.3
        for _ in range(itr):
            idx = math.floor(random.randint(0, len(self._format) - 1 )) # pick a random index
            path = self._format[idx]
            # ideas: either conform to the type or dont. For now I will not conform
            self._format[idx] = (path, None)

if __name__ == "__main__":
    nested_json = {
        "user": {
            "id": 101,
            "profile": {
                "name": "Alice",
                "active": True
            },
            "tags": ["admin", "tester"]
        },
        "timestamp": "2023-10-27"
    }
    flat = Json._flatten(nested_json, sep=".")
    print(flat)