import subprocess
import math
import random
import time
from pathlib import Path
from mutators import json_csv_mutator
from colours import Colours
import agnostic_mutator
from parser import parser

RUN_TIME_PER_BINARY = 60000 #ms

def fuzzBinary(binary: Path, sample_input: Path):
    start_time = time.time()
        
    # TODO: using multiprocessing for multiple threads

    # TODO: capture any other output by the binary such as stderr, library calls etc

    # read the input from example
    with open(sample_input, 'rb') as file:
        file_content = file.read()

    i = 0
    while True:
        random.seed(i)
        
        execution_time = (time.time() - start_time) * 1000
        if execution_time > RUN_TIME_PER_BINARY:
            print(f"{Colours.BOLD}{Colours.RED}{RUN_TIME_PER_BINARY}ms have elapsed, moving onto next binary                                         {Colours.RESET}")
            break
            
        input_bytes = parser(sample_input, file_content, seed=i)
        
        command_output = subprocess.run(binary,
                                        input=input_bytes, capture_output=True) 
        
        if command_output.returncode != 0:
            print(f"{Colours.BOLD}{Colours.GREEN}The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, \
which is {i//(execution_time/1000)} attempts/s to find the input\n \
{Colours.CYAN}{input_bytes[:200]}{Colours.RESET}\n {Colours.BOLD}{Colours.GREEN}which crashes the program{Colours.RESET}")
            
            # write output to file
            with open(f'fuzzer_output/bad_{binary.name}.txt', 'wb') as file:
                file.write(input_bytes)
            
            return True
        
        if i % 501 == 0 and i != 0:
            execution_time = (time.time() - start_time)
            print(f"{i}: \t{i//(execution_time)} attempts/s \tinput: {input_bytes[:50]}", end='\r')
        
        i += 1