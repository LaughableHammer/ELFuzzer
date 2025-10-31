# Fuzzer Description
The fuzzer consists of 2 main components:
1. Harness -> Execute payloads on each binary and determine if this results in an interesting behaviour (crash, invalid memory write, heap UF etc.)
2. Mutator -> Perform various mutation strategies on the sample input to seed interesting behaviour

Our fuzzer currently uses the following mutation strategies:
- For plain text files
    - String mutation:
        - Try changing given string in parts with the given mutation index
    - Format-string fuzzing
        - Try format string specifiers to check for format string vulnerabilities

- For CSV/Json
    - Extending
        - 'Extends' the input by duplicates the provided input between 0 and 5 times

    - Add
        - Randomly extends input fields by adding ASCII characters

It also utilises a corpus to mutate the sample input, and then perform further mutations on the mutated input itself, allowing for more diverse inputs that vary significantly from the initial sample. This corpus is trimmed when it gets too big and occasionally, the sample input is added back to it to ensure we don't stray too far from the expected format.

The harness locates the provided binaries and associated inputs, and depending on the input file type, it will send it to the appropriate mutator. The mutated input is then provided back to the harness which runs the binary and feeds it the input, monitoring for an incorrect program state to occur. 

The fuzzer can find bugs with how CSVs and JSON files are parsed, it can look for buffer overflows in text and csv and json files by modifying random values to be very large. It can also detect format string vulnerabilities in plaintext input binaries by placing crash inducing format specifiers randomly in the input.

# Improvements 

- Add a parser to the current fuzzer structure - facilitate the input mutation process by ensuring that file format is maintained and a valid input is given as currently, a small percentage of the inputs provided to the binaries may break formatting (delete a comma in a csv) which results in wasted CPU cycles and time.

- Add more mutation strategies such as magic strings and bit flipping