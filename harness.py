import subprocess
import math
import random
import time
from pathlib import Path
from colours import Colours
from parser import parser
from flask_socketio import SocketIO, emit

# import agnostic_mutator

BASE_RUN_TIME_PER_BINARY = 60000  # ms
BASE_TIMEOUT = 3                 # seconds

ERRORS_EXPECTED = {
    -4: b"Illegal instruction",             # SIGILL
    -5: b"Trace/breakpoint trap",           # SIGTRAP
    -6: b"stack smashing",                  # SIGABRT
    -7: b"Bus error",                       # SIGBUS
    -8: b"Floating point exception",        # SIGFPE
    -11: b"Segmentation fault",             # SIGSEGV
    -12: b"Bad system call",                # SIGSYS (seccomp)
    -31: b"Bad system call",                # SIGSYS on some kernels
}


def fuzzBinary(binary: Path, sample_input: Path, timeout=BASE_TIMEOUT, 
               run_time_per_binary=BASE_RUN_TIME_PER_BINARY, updateWebsite=False) -> bool:
    start_time = time.time()

    # TODO: using multiprocessing for multiple threads
    # TODO: capture any other output by the binary such as stderr, library calls etc

    # read the input from example
    with open(sample_input, "rb") as file:
        file_content = file.read()

    i = 0
    while True:
        random.seed(i)

        execution_time = (time.time() - start_time) * 1000
        if execution_time > run_time_per_binary:
            print(
                f"{Colours.BOLD}{Colours.RED}{run_time_per_binary}ms have elapsed, moving onto next binary                                         {Colours.RESET}"
            )
            break

        input_bytes = parser(sample_input, file_content, seed=i)
        try:
            command_output = subprocess.run(
                binary, input=input_bytes, capture_output=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            print("Timed out. Infinite loop detected")
            return False  # Consider returning true

        if command_output.returncode < 0:
            if (
                ERRORS_EXPECTED[command_output.returncode] not in command_output.stderr
                and command_output.stderr
            ):
                print(
                    f"{Colours.MAGENTA}stderr output {command_output.stderr[:50]} {command_output.stdout[:50]} {command_output.returncode} does not match error code, ignoring{Colours.RESET}"
                )

            print(f"{Colours.BOLD}{Colours.GREEN}The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, which is {i//(execution_time/1000)} attempts/s to find the input")
            print(f"{Colours.CYAN}{input_bytes[:200]}{Colours.RESET}\n {Colours.BOLD}{Colours.GREEN}which crashes the program{Colours.RESET}")

            if command_output.returncode in ERRORS_EXPECTED:
                error_text = ERRORS_EXPECTED[command_output.returncode]
            else:
                error_text = b""
            print(
                f"{Colours.YELLOW}Error {command_output.returncode} {error_text.decode('utf-8')} detected.\nstderr: {command_output.stderr.strip()}{Colours.RESET}"
            )

            # write output to file
            with open(f"fuzzer_output/bad_{binary.name}.txt", "wb") as file:
                file.write(input_bytes)

            return True

        if i % 501 == 0 and i != 0:
            execution_time = time.time() - start_time
            print(
                f"{i}: \t{i//(execution_time)} attempts/s \tinput: {input_bytes[:50]}",
                end="\r",
            )

        i += 1
