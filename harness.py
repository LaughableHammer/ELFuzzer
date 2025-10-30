"""Main program that the Dockerfile directly loads: controls fuzzer's operations"""
import subprocess
import math
import random
import time
from pathlib import Path
from fileformat import Plaintext, Csv
from mutator import mutate
from colours import Colours

# binaries are here
#binaries = Path('binaries/')

# Use this for testing
binaries = [Path('binaries/passcode1'), Path('binaries/csv1'), Path('binaries/json1')]

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
    input_format = sample_input.name[:-5] # strip extension and number
        
    # TODO: Many more things to do such as having a timeout, 
    # and using multiprocessing for multiple threads

    # TODO: capture any other output by the binary such as stderr, library calls etc

    # read the input from example
    with open(sample_input, 'r') as file:
        file_content = file.read()

    match input_format:
        case 'passcode':
            file_format = Plaintext(file_content)
        case 'plaintext':
            file_format = Plaintext(file_content)
        case 'csv':
            # file_format = Csv() # TODO
            continue
        case 'json':
            # file_format = Json() # TODO
            continue

    i = 0
    while True:
        file_format = Plaintext(file_content)
        mutated_input = file_format.encode(mutate(file_format.parse(), i))
        input_bytes = (mutated_input + "\n").encode()
        
        command_output = subprocess.run(binary,
                                        input=input_bytes, capture_output=True)

        # TODO proper CLI UI and statistics will be displayed here -
        # probably as a function call
        if command_output.returncode != 0:
            execution_time = (time.time() - start_time) * 1000
            print(f"{Colours.BOLD}{Colours.GREEN}The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, \
which is {i//(execution_time/1000)} attempts/s to find the input \
{mutated_input} which crashes the program{Colours.RESET}")
            
            # write output to file ie /fuzzer_output/{binary}.txt
            with open(f'fuzzer_output/bad_{binary.name}.{file_format.fileFormat()}', 'w') as file: file.write(mutated_input)
            
            break

        if i % 501 == 0 and i != 0:
            execution_time = (time.time() - start_time)
            print(f"{i}: \t{i//execution_time} attempts/s \tinput: {mutated_input}", end='\r')

        i += 1
