"""
Testing json libraries
"""
from flatten_dict import flatten, unflatten
import json
import random
import string

def util_gen_random_str(len = 5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class Json:
    """
    File format representing a JSON file. 

    TODO: consider if file handling should be done here
    """
    def __init__(self, _file:str):
        """
        Parse the provided file.
        """
        with open(_file, "r") as f:
            json_dict = json.loads(f.read())
            self._format = flatten(json_dict, reducer='dot')

    @staticmethod
    def parse(data):
        json_dict = json.loads(data)
        return flatten(json_dict)
    
    def encode(self) -> bytearray:
        """
        Turns the parsed format into JSON string object again

        Possibly use a flatdict library that creates a flattened dictionary
        """        
        json_dict = unflatten(self._format, splitter="dot")
        return json.dumps(json_dict)
    
    def _debug_dump(self):
        print(self._format)

    def _debug_dump_pretty(self):
        print(json.dumps(unflatten(self._format, splitter='dot'), indent=4))


    # @staticmethod
    def mutate(self):
        """
        Takes itself and calls one of the mutate functions
        """
        strategies = [
            Json._mutate_duplicate,
            Json._mutate_change_entry,
            Json._mutate_change_key,
            Json._mutate_add_depth,
            Json._mutate_add_branch,
            Json._mutate_add_entry,
            Json._mutate_remove_entries,
            Json._mutate_set_null,
        ]
        strat_used = random.choice(strategies)
        print(strat_used)
        strat_used(self)
    
    @staticmethod
    def _mutate_duplicate(self):
        """
        Duplicates some entry somewhere to a random location, with depth 0 - n+1
        Takes two choices from the tuple, one to get a random path, the other a value. 
        Path is mutated to avoid mutation, by appending 

        # TODO: consider if duplicate will copy and replace, or just copy and put.
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 1):
            itr = random.randint(0, 10)
        key_list = list(self._format.keys())
        value_list = list(self._format.values())
        for _ in range(itr):
            path = random.choice(key_list) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            value = random.choice(value_list)
            self._format[path] = value
    
    @staticmethod
    def _mutate_change_entry(self):
        """
        Picks 30% of all entries and then changes to some random bytes.
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 5):
            itr = random.randint(0, 3)
        key_list = list(self._format.keys())
        for _ in range(itr):
            path = random.choice(key_list)
            
            # either change it to a list or a string. Either randomly or according to previous data type.
            if isinstance(self._format[path], list):
                value = []
                for i in range(len(self._format[path]) + random.randint(0, 5)):
                    # value.append(random.randbytes(5))
                    value.append(util_gen_random_str(10))
            else:
                # value = random.randbytes(10) # for now bytes do not work and wlil crash.
                value = util_gen_random_str(100)
            self._format[path] = value
        # determine if a return object is wanted or just change in place
           
    
    @staticmethod
    def _mutate_add_depth(self):
        pass
        """
        Make the JSON object deeper, using random generated keys (or duplicate)
        Values will be set to some random generic alphanumerical string
        Note: this may cause rabbit holing if there are multiple choices of deepness.
        TODO: support for list
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 5):
            itr = random.randint(0, 3)
        key_list = list(self._format.keys())
        for _ in range(itr):
            # TODO: gotta finish
            pass
            
    @staticmethod
    def _mutate_add_branch(self):
        """
        Add a JSON object somewhere, enabling more branches
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 5):
            itr = random.randint(0, 7)
        for _ in range(itr):
            nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            key_list = list((self._format).keys())
            path_arr = random.choice(key_list).split(".")
            if len(path_arr) == 1:
                path = '' + nonce
            else:
                n = len(path_arr)
                c = random.randint(0, n - 1)
                path = path_arr[:c]
                path = ".".join(path)
                if (not path):
                    path = nonce
                else:
                    path = path + "." + nonce
            self._format[path] = {}

    
    @staticmethod
    def _mutate_add_entry(self):
        """
        Adds an entry at a random location, including in the middle of extensive paths.
        This includes adding lists.
        TODO: add support for adding numerical values. 
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 5):
            itr = random.randint(0, 7)
        for _ in range(itr):
            if random.random() < 0.25:
                if random.random() > 0.5:
                    value = util_gen_random_str()
                else:
                    value = random.randint(0, 1000)
            else:
                value = []
                for i in range(random.randint(0, 10)):
                    value.append(util_gen_random_str())

            nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            key_list = list((self._format).keys())

            path_arr = random.choice(key_list).split(".")
            # cut the path, to simulate a depth
            # Edge case: path of length 1
            # 
            if len(path_arr) == 1:
                path = '' + nonce
            else:
                n = len(path_arr)
                c = random.randint(0, n - 1)
                path = path_arr[:c]
                path = ".".join(path)
                if (not path):
                    path = nonce
                else:
                    path = path + "." + nonce
            self._format[path] = value
    
    @staticmethod
    def _mutate_change_key(self):
        """
        Change the key of a JSON object to a random string.

        # TODO: consider changing to a byte obj rather than string.
        """
        itr = int(len(self._format) * 0.1)
        if (itr < 5):
            itr = random.randint(0, 7)
        
        for _ in range(itr):
            # find a key
            key_list = list(self._format.keys())

            key = random.choice(key_list)          
            value = self._format[key]

            del self._format[key] # remove the the K:V pair
            
            key_part = key.split(".")
            idx = random.randint(0, len(key_part) - 1)

            key_part[idx] = util_gen_random_str()
            key = ".".join(key_part)

            self._format[key] = value
            
    
    @staticmethod    
    def _mutate_remove_entries(self):
        """
        remove items entirely
        """
        itr = int(len(self._format) * 0.1) #TODO: remove this repetitive code?? It is one line though..
        if itr < 1:
            itr = 1
        for _ in range(itr):
            key_list = list(self._format.keys())
            to_del = random.choice(key_list)
            del self._format[to_del]
    
    @staticmethod
    def _mutate_set_null(self):
        """
        Makes certain entries blank
        """
        key_list = list(self._format.keys())
        itr = int(len(self._format) * 0.1)
        if itr < 1:
            itr = random.randint(0, 10)
        for _ in range(itr):
           # find a random key and then change the value to null
           # TODO: check that this actually sets as null
           self._format[random.choice(key_list)] = "null"


nested_dict =  {'data': {'name': 'Alice', 'details': {'age': 30, 'food':['apple', 'burger']}}}
p = "./example_inputs/json1.txt"
obj = Json(p)

# fuzzer fuzzer
for i in range(1000):
    """
    Current this takes ages to do 1000 mutation... <insert time>, getting slower along the way. 
    This may be because 1: my computer is slow and 2: the JSON object is getting massive and `itr` variable is exploding.
    """
    obj.mutate()

obj._debug_dump_pretty()

# d = "./depth.txt"
# obj = Json(d)

# obj._mutate_duplicate()
# obj._mutate_change_entry()
# obj._mutate_add_entry()

# print(obj.encode())
