import random
import globalVar
from .common_mutators import additive, extend
import copy
<<<<<<< HEAD
=======
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

    if obj.object_id is not None:
        if obj.object_id in seen:
            return
        seen.add(obj.object_id)

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
            print(data)
            # data = data.replace(old, new)
            # stream.write(data)         # pikepdf auto-recompresses if needed

    return encode_pdf(pdf)



def _mutate_replace_number(pdf_bytes: bytes) -> bytes:
    strings = []

    def mask(m):
        return b"a" * (m.end() - m.start())

    pdf_without_streams = re.sub(rb"stream.*?endstream", mask, pdf_bytes, flags=re.S)

    numbers = list(re.finditer(rb"\b\d+\.\d+\b", pdf_without_streams))

    number_to_replace = random.choice(numbers)

    start, end = number_to_replace.start(), number_to_replace.end()

    # TODO: pick random number
    mutated_bytes = pdf_bytes[:start] + b"67" + pdf_bytes[end:]

    return mutated_bytes

>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c

def pdf_mutate(sample_input: bytes) -> bytes:
    if not globalVar.corpus:
        globalVar.corpus.append(sample_input)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(sample_input)
<<<<<<< HEAD
=======

    strategies = [
        _mutate_replace_number
    ]

>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
