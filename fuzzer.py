from pathlib import Path
from harness import fuzzBinary
from colours import Colours
import time
import globalVar

# binaries are here
binaries = Path('binaries/')

# for additional testing
# binaries = Path('created_binaries/')

overall_start = time.time()

results = []

for binary in binaries.iterdir():
    globalVar.init() # Reset global values
    print(f"{Colours.UNDERLINE}Fuzzing binary: {binary.name}{Colours.RESET}")
    

    sample_input = Path(f'example_inputs/{binary.name}.txt')
    if not sample_input.exists():
        print(f"{Colours.RED}Could not find sample input{Colours.RESET}")
        continue

    print("Sample input file:", sample_input)
    
    start_time = time.time()
    fuzzed = fuzzBinary(binary, sample_input)
    elapsed = time.time() - start_time
    
    results.append((binary.name, fuzzed, elapsed))

total_time = time.time() - overall_start
total_binaries = len(results)
fuzzed_count = sum(1 for _, success, _ in results if success)
avg_time = total_time / total_binaries if total_binaries > 0 else 0

print("\n" + "=" * 60)
print(f"{Colours.BOLD}{Colours.UNDERLINE}FUZZING SUMMARY{Colours.RESET}")
print(f"Total binaries processed: {total_binaries}")
print(f"Successfully fuzzed:      {fuzzed_count}")
print(f"Total time:               {total_time:.2f} seconds")
print(f"Average time per binary:  {avg_time:.2f} seconds")