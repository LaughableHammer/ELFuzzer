from pathlib import Path
from harness import fuzzBinary
from colours import Colours
import time

# binaries are here
#binaries = Path('binaries/')

# Use this for testing
binaries = [Path('binaries/passcode1'), Path('binaries/csv1'), Path('binaries/json1'), Path('binaries/csv2')]


start_time = time.time()

#for binary in binaries.iterdir():
for binary in binaries:
    print(f"{Colours.UNDERLINE}Fuzzing binary: {binary.name}{Colours.RESET}")
    
    sample_input = Path(f'example_inputs/{binary.name}.txt')
    if sample_input.exists():
        print("Sample input file:", sample_input)
    else:
        print(f"{Colours.RED}Could not find sample input{Colours.RESET}")
        continue
    
    fuzzed = fuzzBinary(binary, sample_input)