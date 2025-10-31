# Fuzzer Description
The fuzzer consists of 2 main components:
1. Harness -> Execute payloads on each binary and determine if this results in an interesting behaviour (crash, invalid memory write, heap UF etc.)
2. Mutator -> Perform various mutation strategies on the sample input to seed interesting behaviour

Our fuzzer currently uses the following mutation strategies:
For plain text files
String mutation:
- Try changing given string in parts with the given mutation index
Format-string fuzzing
- Try format string specifiers to check for format string vulnerabilities

For CSV/Json
Extending
- 'Extends' the input by duplicates the provided input between 0 and 5 times

Add
- Randomly extends input fields by adding ASCII characters

The harness locates the provided binaries and associated inputs, and depending on the input file type, it will send it to the appropriate mutator. The mutated binary is then provided back to the harness which runs the binary and feeds it the input, monitoring for an incorrect program state to occur. 

Currently, the fuzzer doesn't adapt its strategy depending on the binary or output of already run inputs, so it is "dumb". It also doesn't look for any additional branches in input which might allows more vectors for exploitation. 

# Improvements 

- Add a parser to the current fuzzer structure - facilitate the input mutation process by ensuring that file format is maintained and a valid input is given as currently we provide invalid input to the fuzzer

- Add more mutation strategies