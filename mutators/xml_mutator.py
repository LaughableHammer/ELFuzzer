"""
A mutator for xmls
"""
import random
from lxml import etree
import globalVar
import copy
import string
from mutators.common_mutators import mutate

def util_gen_random_str(len = 999):
    return ''.join(random.choices(string.ascii_uppercase, k=len))

def xml_mutate(tree):
    if not globalVar.corpus:
        globalVar.corpus.append(tree)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    if random.random() < 0.5:
        globalVar.corpus.append(tree)
    
    src = random.choice(globalVar.corpus)
    mutated = copy.deepcopy(src)
    mutation_strategies = [
        add_node,
        # del_node,
        # change_node, # broken
        change_attr,
        change_root,
        change_tag,
        # add_depth,
    ]

    # Consider if there should be a few rounds of mutation?
    chosen = random.choice(mutation_strategies)
    # print(chosen)
    mutated = chosen(mutated)

    if random.random() < 0.1:
        globalVar.corpus.insert(0, mutated)
    else:
        globalVar.corpus.append(mutated)
    return mutated

def add_node(tree):
    """
    Add a node with arbitrary value, tag and class
    """
    for _ in range(0, random.randint(0, 50)):
        new = etree.Element(util_gen_random_str(10))
        # new.text = util_gen_random_str(10)
        payload = mutate(bytearray(util_gen_random_str(1), "utf-8"))
        try:
            new.text = payload
        except:
            new.text = payload.hex()
        random_idx = random.randint(0, max(0, len(tree) - 1))
        tree.insert(random_idx, new)
    return tree

def del_node(tree):
    """
    Delete a percentage number of node, as long as 
    they are not the root noded
    """
    itr = int(len(tree) * 0.3)
    if itr < 1:
        itr = random.randint(0, len(list(tree)))
    to_delete = random.sample(list(tree), itr)

    for node in to_delete:
        parent = node.getparent()
        parent.remove(node)
    
    return tree

def change_node(tree):
    """
    Change the node content
    """
    itr = int(len(tree) * 0.3)
    if itr < 1:
        itr = random.randint(1, (len(list(tree))))

    to_change = random.sample(list(tree), itr)
    for node in to_change:
        if len(node.text.strip()) < 0:
            continue
        node.text = mutate(bytearray(node.text, "utf-8")).hex()
    return tree

def add_attr(tree):
    """
    Add an attribute to an XML object. 
    Consider whether this would be artbirary or predefined attributes
    """
    node = random.choice(tree)
    node.attrib[util_gen_random_str()] = mutate(util_gen_random_str())
    return tree

def change_attr(tree):
    """
    Change the attributes of some XML objects, other that root node.

    Most likely will include custom logic to handle websites and urls for hrefs or what not
        - This case can simply be just adding random printable bytes
    """
    node = random.choice(list(tree.iter()))

    if not node.attrib:
        return tree
    
    key = random.choice(list(node.attrib.keys()))
    try:
        node.attrib[key] = mutate(bytearray(node.attrib[key], "utf-8")).decode(errors='ignore')
    # node.attrib[key] = util_gen_random_str(100)
    except:
        return tree
    return tree

def remove_attr(tree):
    """
    Remove the attribute of random objects
    """
    node = random.choice(tree)
    key_list = list(node.attrib.keys())
    node.attrib.pop(random.choice(key_list), None)
    return tree

def change_tag(tree):
    """
    Changes the tag of a node
    """
    itr = int(len(tree) * 0.3)
    if itr < 1:
        itr = random.randint(0, len(list(tree)))
    to_change = random.sample(list(tree), itr)

    for node in to_change:
        node.tag = util_gen_random_str(3)
    
    return tree

def change_root(tree):
    """
    Change the root node of the tree to be another string.
    Should be used rarely
    """
    root = list(tree.iter())[0]
    root.tag = util_gen_random_str(random.randint(1, 4))
    return tree

def swap_order(tree):
    """
    Switches the order between two or more nodes
    """
    a, b = random.sample(tree, 2)
    a_parent = a.getparent()
    b_parent = b.getparent()

    a_idx = a_parent.index(a)
    b_idx = b_parent.index(b)

    a_parent[a_idx] = b
    b_parent[b_idx] = a

def add_depth(tree):
    """
    Adds some depth to the tree
    """
    itr = random.randint(0, 30)
    for _ in range(itr):
        chosen_parents = random.choice(tree)
        child = etree.Element(util_gen_random_str(100))
        payload = mutate(bytearray(util_gen_random_str(5), "utf-8"))
        try:
            child.text = payload
        except:
            child.text = payload.hex()
        
        child_depth = random.randint(0, 20)
        current = child

        for _ in range(child_depth):
            sub_child = etree.Element(util_gen_random_str(10))
            sub_payload = mutate(bytearray(util_gen_random_str(10), "utf-8"))
            try:
                sub_child.text = sub_payload
            except:
                sub_child.text = sub_payload.hex()
            
            current.append(sub_child)
            current = sub_child
        chosen_parents.append(child)
    return tree

def debug(tree):
    tree = etree.fromstring(tree)

    for node in tree.iter(): # this is likely how the tree would be iterated
        print(node)
