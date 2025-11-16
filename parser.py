from pathlib import Path
from io import StringIO # allows dealing with file-like objects in memory
import agnostic_mutator
import globalVar
import json, csv
import xml.etree.ElementTree as etree
from mutators.csv_mutator import csv_mutate
from mutators.json_mutator import mutate
from flatten_dict import flatten, unflatten
import random

def decode_bytes(b: bytes) -> str:
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1", errors="ignore") # allows everything

def detect_filetype(input_path: Path):
    if globalVar.filetype:
        return globalVar.filetype

    # Read once
    text = decode_bytes(input_path.read_bytes()).strip()

    # Check JSON (only accept dicts or lists)
    if text and text[0] in ('{', '['):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, (dict, list)):
                globalVar.filetype = 'json'
                print(f"File type detected: {globalVar.filetype}")
                return globalVar.filetype
        except Exception:
            pass

    # Check CSV
    try:
        with open(input_path, 'r', newline='', encoding='utf-8', errors='ignore') as f:
            sample = f.read(1024)
            if '\n' in sample and ',' in sample:  # must have multiple lines to be plausible CSV
                csv.Sniffer().sniff(sample)
                globalVar.filetype = 'csv'
                print(f"File type detected: {globalVar.filetype}")
                return globalVar.filetype
    except Exception:
        pass

    # Check XML
    if text.startswith('<'):
        try:
            etree.fromstring(text)
            globalVar.filetype = 'xml'
            print(f"File type detected: {globalVar.filetype}")
            return globalVar.filetype
        except Exception:
            pass

    # Default to plaintext
    globalVar.filetype = 'plaintext'
    print(f"Defaulting: {globalVar.filetype}")
    return globalVar.filetype

def csv_to_rows(csv_text: str) -> list[list[str]]:
    f = StringIO(csv_text)
    reader = csv.reader(f)
    return [row for row in reader]

def rows_to_csv(rows: list[list[str]]) -> str:
    f = StringIO()
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)
    return f.getvalue()

def json_parser(text: str) -> str:
    json_dict = flatten(json.loads(text))
    mutated = mutate(json_dict)
    return unflatten(mutated, splitter="dot")

def csv_parser(text: str) -> str:
    """Parse CSV text → mutate structured rows → return mutated CSV string."""
    # convert into 2d array
    try:
        rows = csv_to_rows(text)
    except Exception:
        rows = [[text]]

    # mutate
    mutated_rows = csv_mutate(rows)

    # convert to str
    mutated_csv_text = rows_to_csv(mutated_rows)

    #with open('output.bin', 'ab') as f: f.write(f'======New Output======\n{mutated_csv_text}\n'.encode())

    return mutated_csv_text + "\n"

def plaintext_parser(input: list[str], seed: int) -> str:
    return agnostic_mutator.plaintext_mutate(input, seed)


def parser(input_path: Path, file_content: bytes, seed: int) -> bytes:
    ft = detect_filetype(input_path)

    # Modify inputs to the functions as desired.
    match ft:
        case "csv":
            text = file_content.decode(errors='ignore')
            return (csv_parser(text) + '\n').encode()
            # parts = [file_content.decode(errors='ignore')]
            # return (json_parser(parts, seed) + '\n').encode()
        case "json":
            parts = file_content.decode(errors='ignore')
            return (json_parser(parts) + '\n').encode()
        case _:
            # assume plaintext if no match
            parts = [file_content.decode(errors='ignore')]
            return (plaintext_parser(parts, seed) + '\n').encode()