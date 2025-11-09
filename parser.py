from pathlib import Path
from mutators import json_csv_mutator
import agnostic_mutator
import globalVar
from colours import Colours
import json, csv
import xml.etree.ElementTree as etree


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

    # Check JSON (only accept dicts or lists, not primitives like 1, "abc", etc.)
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
            if '\n' in sample:  # must have multiple lines to be plausible CSV
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

def json_parser(parts: list[str], seed: int) -> str:
    mutated = json_csv_mutator.json_csv_mutate(parts, seed)
    return ''.join(mutated)

def csv_parser(parts: list[str], seed: int) -> str:
    mutated = json_csv_mutator.json_csv_mutate(parts, seed)
    return ''.join(mutated)

def plaintext_parser(input: list[str], seed: int) -> str:
    return agnostic_mutator.plaintext_mutate(input, seed)


def parser(input_path: Path, file_content: bytes, seed: int) -> str:
    ft = detect_filetype(input_path)
    #globalVar.filetype = input_path.name[:-5]

    # Modify inputs to the functions as desired.
    match ft:
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