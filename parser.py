from pathlib import Path
from mutators import json_csv_mutator
import agnostic_mutator
import globalVar
from colours import Colours

def json_parser(parts: list[str], seed: int) -> str:
    mutated = json_csv_mutator.json_csv_mutate(parts, seed)
    return ''.join(mutated)

def csv_parser(parts: list[str], seed: int) -> str:
    mutated = json_csv_mutator.json_csv_mutate(parts, seed)
    return ''.join(mutated)

def plaintext_parser(input: list[str], seed: int) -> str:
    return agnostic_mutator.plaintext_mutate(input, seed)


def parser(input_path: Path, file_content: bytes, seed: int) -> str:
    if globalVar.filetype:
        next
    else:
        # Replace this with actual parsing logic to infer file type based on contents/signature
        globalVar.filetype = input_path.name[:-5]

    # Modify inputs to the functions as desired.
    match globalVar.filetype:
        case "json":
            parts = [file_content.decode(errors='ignore')]
            return (json_parser(parts, seed) + '\n').encode()
        case "csv":
            parts = [file_content.decode(errors='ignore')]
            return (json_parser(parts, seed) + '\n').encode()
        case _:
            # assume plaintext if no match
            parts = [file_content.decode(errors='ignore')]
            return (plaintext_parser(parts, seed) + '\n').encode()