import random
import globalVar
from .common_mutators import additive, extend
import copy

def pdf_mutate(sample_input: bytes) -> bytes:
    if not globalVar.corpus:
        globalVar.corpus.append(sample_input)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(sample_input)
