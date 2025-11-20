"""
Testing json libraries
"""
from flatten_dict import unflatten
import globalVar
import random
import string
import json
import copy

def util_gen_random_str(len = 5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=len))

def mutate(data: dict) -> dict:
    """
    Takes data and calls one of the mutate functions
    """
    if not globalVar.corpus:
        globalVar.corpus.append(data)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(data)

    src = copy.deepcopy(random.choice(globalVar.corpus))
    strategies = [
        _mutate_duplicate,
        _mutate_change_entry,
        _mutate_change_key,
        _mutate_add_depth,
        _mutate_add_branch,
        _mutate_add_entry,    
        _mutate_remove_entries,
        _mutate_set_null,
    ]
    strat_used = random.choice(strategies)
    mutated_data = strat_used(src)

    if random.random() < 0.1:
        globalVar.corpus.insert(0, mutated_data)
    else:
        globalVar.corpus.append(mutated_data)
    
    return mutated_data

def _mutate_duplicate(data):
    """
    Duplicates some entry somewhere to a random location, with depth 0 - n+1
    Takes two choices from the tuple, one to get a random path, the other a value. 
    Path is mutated to avoid mutation, by appending 

    # TODO: consider if duplicate will copy and replace, or just copy and put.
    """
    itr = int(len(data) * 0.1)
    if (itr < 1):
        itr = random.randint(0, 10)
    
    key_list = list(data.keys())
    value_list = list(data.values())
    
    for _ in range(itr):
        path = random.choice(key_list) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        value = random.choice(value_list)
        data[path] = value
    
    return data
    

def _mutate_change_entry(data: list) -> list:
    """
    Picks 30% of all entries and then changes to some random bytes.
    """
    itr = int(len(data) * 0.1)
    if (itr < 5):
        itr = random.randint(0, 3)
    key_list = list(data.keys())
    for _ in range(itr):
        path = random.choice(key_list)
        
        # either change it to a list or a string. Either randomly or according to previous data type.
        if isinstance(data[path], list):
            value = []
            for _ in range(len(data[path]) + random.randint(0, 5)):
                # value.append(random.randbytes(5))
                value.append(util_gen_random_str(10))
        elif isinstance(data[path], str):
            # value = random.randbytes(10) # for now bytes do not work and will crash.
            value = util_gen_random_str(10)
        elif isinstance(data[path], int):
            value = random.randint(0, 999)
        else:
            value = util_gen_random_str(10)
        data[path] = value
    # determine if a return object is wanted or just change in place
    return data
           
def _mutate_add_depth(data):
    return data
    """
    Make the JSON object deeper, using random generated keys (or duplicate)
    Values will be set to some random generic alphanumerical string
    Note: this may cause rabbit holing if there are multiple choices of deepness.
    TODO: support for list
    """
    itr = int(len(data) * 0.1)
    if (itr < 5):
        itr = random.randint(0, 3)
    key_list = list(data.keys())
    for _ in range(itr):
        # TODO: gotta finish
        pass
            
def _mutate_add_branch(data):
    """
    Add a JSON object somewhere, enabling more branches
    """
    itr = int(len(data) * 0.1)
    if (itr < 5):
        itr = random.randint(0, 7)
    for _ in range(itr):
        nonce = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        key_list = list((data).keys())
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
        data[path] = {
            util_gen_random_str(): util_gen_random_str()
        }
    return data

def _mutate_add_entry(data):
    """
    Adds an entry at a random location, including in the middle of extensive paths.
    This includes adding lists.
    TODO: add support for adding numerical values. 
    """
    itr = int(len(data) * 0.1)
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
        key_list = list((data).keys())

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
        data[path] = value
    return data
    
def _mutate_change_key(data):
    """
    Change the key of a JSON object to a random string.

    # TODO: consider changing to a byte obj rather than string.
    """
    itr = int(len(data) * 0.1)
    if (itr < 5):
        itr = random.randint(0, 7)
    
    for _ in range(itr):
        # find a key
        key_list = list(data.keys())

        key = random.choice(key_list)          
        value = data[key]

        del data[key] # remove the the K:V pair
        
        key_part = key.split(".")

        key_part[random.randint(0, len(key_part) - 1)] = util_gen_random_str()
        key = ".".join(key_part)

        data[key] = value
    return data
    
def _mutate_remove_entries(data):
    """
    remove items entirely
    """
    itr = int(len(data) * 0.1) #TODO: remove this repetitive code?? It is one line though..
    if itr < 1:
        itr = 1
    for _ in range(itr):
        key_list = list(data.keys())
        to_del = random.choice(key_list)
        del data[to_del]
    return data
    

def _mutate_set_null(data):
    """
    Makes certain entries blank
    """
    key_list = list(data.keys())
    itr = int(len(data) * 0.1)
    if itr < 1:
        itr = random.randint(0, 10)
    for _ in range(itr):
        # find a random key and then change the value to null
        # TODO: check that this actually sets as null
        data[random.choice(key_list)] = "null"
    return data