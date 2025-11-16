import subprocess
import math
import random
import time
import os
import sys
from pathlib import Path
from mutators import json_csv_mutator
from colours import Colours
import agnostic_mutator
from parser import parser

RUN_TIME_PER_BINARY = 5000 #ms

ERRORS_EXPECTED = {
    -4:  b"Illegal instruction",       # SIGILL
    -5:  b"Trace/breakpoint trap",     # SIGTRAP
    -6:  b"stack smashing detected",   # SIGABRT (stack canary fail)
    -7:  b"Bus error",                 # SIGBUS
    -8:  b"Floating point exception",  # SIGFPE
    -11: b"Segmentation fault",        # SIGSEGV
    -12: b"Bad system call",           # SIGSYS (seccomp)
    -31: b"Bad system call",           # SIGSYS on some kernels
}

def forkserver_main(read_fd: int, write_fd: int, binary: Path):
    """
    Runs inside the forkserver process
    Waits for inputs, forks and then runs the binary in the child with the input
    """
    while True:
        # Read (manually added) header which says how many bytes to expect
        length_bytes = os.read(read_fd, 4)
        if not length_bytes:
            break

        data = os.read(read_fd, int.from_bytes(length_bytes, 'little'))
        if not data:
            break

        pid = os.fork()
        if pid == 0:
            # Child
            result = subprocess.run(binary, input=data, capture_output=True)
            os._exit(result.returncode)

        # Parent
        _, status = os.waitpid(pid, 0)

        os.write(write_fd, status.to_bytes(4, 'little'))
    
    sys.exit(0)

def try_fuzz(write_fd: int, read_fd: int, data: bytes):
    """Send input to forkserver_main and recieve status code"""
    # Let the process know how many bytes we are sending first
    os.write(write_fd, len(data).to_bytes(4, 'little'))
    os.write(write_fd, data)

    status = int.from_bytes(os.read(read_fd, 4), 'little')

    exitcode = os.WEXITSTATUS(status)
    signalled = os.WIFSIGNALED(status)
    signo = os.WTERMSIG(status) if signalled else None

    return exitcode, signo

def init_forkserver(binary: Path):
    """Starts a persistent forkserver"""
    # Get 2 sets of fd's to read and write to and from the forkserver from the parent
    r_p_to_fs, w_p_to_fs = os.pipe()
    r_fs_to_p, w_fs_to_p = os.pipe()

    # pid 0 = child process
    pid = os.fork()

    if pid == 0:
        # close unecessary fd's in the child
        os.close(w_p_to_fs)
        os.close(r_fs_to_p)
        forkserver_main(r_p_to_fs, w_fs_to_p, binary)

    # not needed in parent
    os.close(r_p_to_fs)
    os.close(w_fs_to_p)

    return pid, w_p_to_fs, r_fs_to_p


def fuzzBinary(binary: Path, sample_input: Path):
    start_time = time.time()
        
    print(f"{Colours.BLUE}* Starting forkserver for {binary}{Colours.RESET}")
    fs_pid, send_fd, recv_fd = init_forkserver(binary)


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
        
        exitcode, signo = try_fuzz(send_fd, recv_fd, input_bytes)
        if exitcode != 0 or signo is not None:
            elapsed = (time.time() - start_time) * 1000
            print("\n--- CRASH FOUND ---")
            print(f"Seed: {i}")
            print(f"Runtime: {elapsed:.2f}ms")
            print(f"Exit code: {exitcode}")
            print(f"Signal: {signo}")
            print(f"Input (first 200 bytes): {input_bytes[:200]}")
            break
        
#         if exitcode < 0:
#             if ERRORS_EXPECTED[command_output.returncode] not in command_output.stderr:
#                 print(f"{Colours.MAGENTA}stderr output does not match error code, ignoring{Colours.RESET}")
#                 continue
#             print(f"{Colours.BOLD}{Colours.GREEN}The fuzzer took {i} attempts and {math.ceil(execution_time)}ms, \
# which is {i//(execution_time/1000)} attempts/s to find the input\n \
# {Colours.CYAN}{input_bytes[:200]}{Colours.RESET}\n {Colours.BOLD}{Colours.GREEN}which crashes the program{Colours.RESET}")
#             print(f"{Colours.YELLOW}Error {command_output.returncode} Detected: {command_output.stderr.strip()}{Colours.RESET}")
            
#             # write output to file
#             with open(f'fuzzer_output/bad_{binary.name}.txt', 'wb') as file:
#                 file.write(input_bytes)
            
            return True
        
        if i % 501 == 0 and i != 0:
            execution_time = (time.time() - start_time)
            print(f"{i}: \t{i//(execution_time)} attempts/s \tinput: {input_bytes[:50]}", end='\r')
        
        i += 1