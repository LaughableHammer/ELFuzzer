import random
import globalVar
from .common_mutators import additive, extend
from elftools.elf.elffile import ELFFile
import copy
from io import BytesIO
import lief

def encode_elf(elf: lief.ELF.Binary) -> bytes:
    builder = lief.ELF.Builder(elf)
    builder.build()
    return bytes(builder.get_build())

<<<<<<< HEAD
=======

>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
def _mutate_dupe_section(elf: lief.ELF.Binary, elf_bytes: bytes) -> bytes:
    section = random.choice(elf.sections)

    section.name += "_duplicate" # pyright: ignore[reportOperatorIssue]
    elf.add(section)

<<<<<<< HEAD
    # name = section.name
    # if type(name) == "bytes":
    #     name = name.decode() # pyright: ignore[reportAttributeAccessIssue]

    # duplicate = lief.ELF.Section(name + "_duplicate") # pyright: ignore[reportOperatorIssue]
    # duplicate.content = list(section.content)

    return encode_elf(elf)
    
def _mutate_within_section(elf: lief.ELF.Binary, elf_bytes: bytes) -> bytes:
    boundaries = []

=======
    return encode_elf(elf)
    
def _mutate_within_section(elf: lief.ELF.Binary, elf_bytes: bytes) -> bytes:
>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
    bio = BytesIO(elf_bytes)
    elftools_elf = ELFFile(bio)
    sections = list(elftools_elf.iter_sections())

    start = 0
    end = 0

    if random.random() < 0.8:
        # pick a section
        section = random.choice(sections)
        start, end = section["sh_offset"], section['sh_offset'] + section['sh_size']
    elif random.random() < 0.3:
        # pick header
        end = sections[1]["sh_offset"]
    elif random.random() < 0.6:
        # pick footer
        start = sections[-1]["sh_offset"] + sections[-1]["sh_size"]
        end = len(elf_bytes) - 1
    else:
        # pick multiple section
        i = random.randint(0, len(sections) - 2)
        section1 = sections[i]
        section2 = random.choice(sections[i+1:])
        start, end = section1["sh_offset"], section2["sh_offset"] + section2["sh_size"]

    # TODO: plaintext mutation between start and end
    return elf_bytes

<<<<<<< HEAD
def _mutate_interesting_fields(elf: lief.ELF.Binary, elf_bytes: bytes) -> bytes:

    

    return encode_elf(elf)

# def _mutate_string(elf: lief.ELF.Binary, elf_bytes: bytes) -> bytes:
    
#     return elf_bytes

def find_strings(elf_bytes: bytes) -> list[str]:
    strings = []
=======


def find_strings(elf_bytes: bytes) -> list[tuple[int, int]]:
    locations = []
>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c

    string_start = 0
    for i, char in enumerate(elf_bytes + b'\x00'):
        if char < 32 or char > 126:
            if i - string_start > 8:
<<<<<<< HEAD
                strings.append(elf_bytes[string_start:i])

            string_start = i+1

    return strings

=======
                locations.append((string_start, i-1))

            string_start = i+1

    return locations
>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c


def elf_mutate(sample_input: bytes, seed: int) -> bytes:
    if not globalVar.corpus:
        globalVar.corpus.append(sample_input)
        globalVar.mutator_state["string_queue"] = find_strings(sample_input)
    elif len(globalVar.corpus) > 20:
        globalVar.corpus = globalVar.corpus[10:]
    elif random.random() < 0.3: #0.3 chance of adding a fresh copy
        globalVar.corpus.append(sample_input)

<<<<<<< HEAD
=======
    lief.logging.disable()

>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
    chosen_input = random.choice(globalVar.corpus)
    elf = lief.parse(chosen_input)

    strategies = [
        _mutate_dupe_section,
        _mutate_within_section,
<<<<<<< HEAD
        # _mutate_add_segment,
=======
>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
    ]

    strat_used = random.choice(strategies)

    if seed > 1000 and len(globalVar.mutator_state["string_queue"]) > 0:
        # Systematically try to place format specifiers into each of the strings
        # strat_used = maybe function from common?
<<<<<<< HEAD
        pass

    mutated_elf_bytes = strat_used(elf, chosen_input) # type: ignore


=======
        string_location = globalVar.mutator_state["string_queue"].pop()
        format_specifier = b"%10000$s"

        mutated_elf_bytes = chosen_input[:string_location[0]] + format_specifier + chosen_input[len(format_specifier) + string_location[0]:]

        return mutated_elf_bytes

    mutated_elf_bytes = strat_used(elf, chosen_input) # type: ignore

>>>>>>> 9bd8813337e6acd175f40eb3a3ae26539b1cf83c
    return mutated_elf_bytes
