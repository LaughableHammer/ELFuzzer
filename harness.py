"""Main program that the Dockerfile directly loads: controls fuzzer's operations"""
import subprocess
import math
import random
import time
from pathlib import Path
from fileformat import Plaintext, Csv
from plaintext_mutator import plaintext_mutate
from json_csv_mutator import json_csv_mutate
from colours import Colours

# binaries are here
#binaries = Path('binaries/')

# Use this for testing
binaries = [Path('binaries/passcode1'), Path('binaries/csv1'), Path('binaries/json1')]

#for binary in binaries.iterdir():
for binary in binaries:
    start_time = time.time()
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
    with open(sample_input, 'rb') as file:
        file_content = file.read()

    i = 0
    while True:
        execution_time = (time.time() - start_time) * 1000
        if execution_time > 60000:
            print(f"{Colours.BOLD}{Colours.RED}60 seconds have elapsed, moving onto next binary                                         {Colours.RESET}")
            break

        parts = [file_content.decode(errors='ignore')]
        if "passcode" in input_format or "plaintext" in input_format:
            mutate = plaintext_mutate
        elif "csv" in input_format or "json" in input_format:
            mutate = json_csv_mutate
        else:
            print(f"{Colours.RED}Unknown input format: {input_format}{Colours.RESET}")
            break
            
        mutated_input = ''.join(mutate(parts, i))
        input_bytes = (mutated_input + "\n").encode()
        
        command_output = subprocess.run(binary,
                                        input=input_bytes, capture_output=True)
        # TODO proper CLI UI and statistics will be displayed here -
        # probably as a function call
        
        if command_output.returncode != 0:
            print(f"{Colours.BOLD}{Colours.GREEN}The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, \
which is {i//(execution_time/1000)} attempts/s to find the input\n \
{Colours.CYAN}{mutated_input}{Colours.RESET}\n {Colours.BOLD}{Colours.GREEN}which crashes the program{Colours.RESET}")
            
            # write output to file ie /fuzzer_output/{binary}.txt
            with open(f'fuzzer_output/bad_{binary.name}.txt', 'wb') as file:
                file.write(mutated_input.encode())
            break
        
        if i % 501 == 0 and i != 0:
            execution_time = (time.time() - start_time)
            print(f"{i}: \t{i//execution_time} attempts/s \tinput: {mutated_input[:50]}", end='\r')
        
        i += 1
