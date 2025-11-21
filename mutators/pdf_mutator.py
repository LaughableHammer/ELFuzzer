import random
import globalVar
from .common_mutators import mutate, get_random_magic_num
import copy
import re

import pikepdf
from io import BytesIO

def parse_pdf(data: bytes):
    bio = BytesIO(data)
    return pikepdf.Pdf.open(bio)

def encode_pdf(pdf: pikepdf.Pdf):
    out = BytesIO()
    pdf.save(out)
    return out.getvalue()

def get_content_streams(obj, seen=None):
    if seen is None:
        seen = set()

    pdf_obj = getattr(obj, "obj", obj)
    obj_id = getattr(pdf_obj, "object_id", None)
    if obj_id is not None:
        if obj_id in seen:
            return
        seen.add(obj_id)

    contents = obj.get("/Contents", None)
    if contents:
        if isinstance(contents, pikepdf.Array):
            for stream in contents:
                if isinstance(stream, pikepdf.Stream):
                    yield stream
        elif isinstance(contents, pikepdf.Stream):
            yield contents

    resources = obj.get("/Resources", None)
    if resources:
        xobjs = resources.get("/XObject", {})
        for x in xobjs.values():
            if isinstance(x, pikepdf.Stream):
                if x.get("/Subtype") == "/Form":
                    yield x
                    for inner in get_content_streams(x, seen):
                        yield inner

def _mutate_replace_text(pdf_bytes: bytes):
    pdf = parse_pdf(pdf_bytes)

    for page in pdf.pages:
        for stream in get_content_streams(page):
            data = stream.read_bytes()  # decompressed  
            stream.write(bytes(mutate(bytearray(data))))

    return encode_pdf(pdf)


def _mutate_replace_number(pdf_bytes: bytes) -> bytes:
    def mask(m):
        return b"a" * (m.end() - m.start())

    pdf_without_streams = re.sub(rb"stream.*?endstream", mask, pdf_bytes, flags=re.S)

    numbers = list(re.finditer(rb"\b\d+\.\d+\b", pdf_without_streams))

    number_to_replace = random.choice(numbers)

    start, end = number_to_replace.start(), number_to_replace.end()

    if random.random() < 0.1:
        number = get_random_magic_num()
    else:
        number = random.randint(-10, 300)
    mutated_bytes = pdf_bytes[:start] + str(number).encode() + pdf_bytes[end:]

    return mutated_bytes


def pdf_mutate(sample_input: bytes) -> bytes:
    if not globalVar.corpus:
        globalVar.corpus.append(sample_input)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(sample_input)

    chosen_input = random.choice(globalVar.corpus)

    strategies = [
        _mutate_replace_number,
        _mutate_replace_text
    ]
    strat_used = random.choice(strategies)

    mutated_elf_bytes = strat_used(chosen_input)

    return mutated_elf_bytes
