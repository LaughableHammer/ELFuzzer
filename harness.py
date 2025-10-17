"""Main program that the Dockerfile directly loads: controls fuzzer's operations"""
import subprocess
import math
import random
import time
from fileformat import Plaintext
from mutator import mutate

# TODO load from folder
binaries = ["passcode"]

start_time = time.time()

for binary in binaries:
    # TODO: Many more things to do such as having a timeout, 
    # and using multiprocessing for multiple threads

    # TODO: capture any other output by the binary such as stderr, library calls etc

    # TODO: read the inputs from a file
    interesting_inputs = ["1", "2"]
    input_weights = [1.0, 0.3]

    i = 0
    while True:
        chosen_input = random.choices(interesting_inputs, weights=input_weights, k=1)[0]

        file_format = Plaintext(chosen_input)
        mutated_input = file_format.encode(mutate(file_format.parse(), i))
        input_bytes = (mutated_input + "\n").encode()
        
        command_output = subprocess.run("./binaries/" + binary,
                                        input=input_bytes, capture_output=True)

        # TODO proper CLI UI and statistics will be displayed here -
        # probably as a function call
        if command_output.returncode != 0:
            execution_time = (time.time() - start_time) * 1000
            print(f"The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, \
which is {i//(execution_time/1000)} attempts/s to find the input \
{mutated_input} which crashes the program")
            
            # TODO: write output to file ie /fuzzer_output/{binary}.txt
            break

        if i % 501 == 0 and i != 0:
            execution_time = (time.time() - start_time)
            print(f"{i}: \t{i//execution_time} attempts/s \tinput: {mutated_input}")

        i += 1
