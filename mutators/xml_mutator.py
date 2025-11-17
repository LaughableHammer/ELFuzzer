"""
A mutator for xmls
"""
import random
from lxml import etree
import globalVar
import copy
import string
from mutators.common_mutators import primitive_mutate

def util_gen_random_str(len = 999):
    return ''.join(random.choices(string.ascii_uppercase, k=len))

def xml_mutate(tree):
    if not globalVar.corpus:
        globalVar.corpus.append(tree)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    
    src = random.choice(globalVar.corpus)
    mutated = copy.deepcopy(src) # I do not know if this will cause performance issues

    mutation_strategies = [
        add_node,
        del_node,
        # change_node, #broken
        change_attr,
        # change_root,
        # change_tag
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
    for _ in range(0, 50):
        new = etree.Element(util_gen_random_str(10))
        new.text = util_gen_random_str(10)
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
        itr = random.randint(1, 5)
    
    to_change = random.sample(list(tree), itr)
    for node in to_change:
        # print(node)
        if len(node.text.strip()) < 0:
            continue
        node.text = primitive_mutate(bytearray(node.text, "utf-8"))
    return tree

def add_attr(tree):
    """
    Add an attribute to an XML object. 
    Consider whether this would be artbirary or predefined attributes
    """
    node = random.choice(tree)
    node.attrib[util_gen_random_str()] = primitive_mutate(util_gen_random_str())
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
    node.attrib[key] = primitive_mutate(bytearray(node.attrib[key], "utf-8"))
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
        node.tag = util_gen_random_str()
    
    return tree

def change_root(tree):
    """
    Change the root node of the tree to be another string.
    Should be used rarely
    """
    root = list(tree.iter())[0]
    root.tag = util_gen_random_str()
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
    pass

def debug(tree):
    tree = etree.fromstring(tree)

    for node in tree.iter(): # this is likely how the tree would be iterated
        print(node)
