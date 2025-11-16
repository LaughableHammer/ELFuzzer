"""
A mutator for xmls
"""
import random
from lxml import etree
import globalVar
import copy

def xmL_mutate(data):
    if not globalVar.corpus:
        globalVar.corpus.append(data)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    
    src = random.choice(globalVar.corpus)
    mutated = copy.deepcopy(src) # I do not know if this will cause performance issues

    mutation_strategies = [
        add_node,
        del_node #todo: include all
    ]

    mutated = random.choice(mutation_strategies)(mutated)

    if random.random() < 0.1:
        globalVar.corpus.insert(0, mutated)
    else:
        globalVar.corpus.append(mutated)
        
    return mutated

def add_node(data):
    """
    Add a node with arbitrary value
    """
    pass

def del_node(data):
    """
    Delete a node
    """
    pass

def change_node(data):
    """
    Change the node content
    """
    pass

def change_attr(data):
    """
    Change the attributes of some XML objects, other that root node.
    """
    node = random.chocie(data)
    if not node.attrib:
        return
    key = random.choice(list(node.attrib.keys()))
    node.attrib[key] = "some-value" 
    pass

def remove_attr(data):
    """
    Remove the attribute of random objects
    """
    pass

def change_tag(data):
    """
    Changes the tag of a node
    """
    pass

def change_root(data):
    """
    Change the root node of the tree to be another string.
    Should be used rarely
    """
    pass

def swap_order(data):
    """
    Switches the order between two or more nodes
    """

def debug(data):
    tree = etree.fromstring(data)

    for node in tree.iter(): # this is likely how the tree would be iterated
        print(node)
