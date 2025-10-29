# Fuzzer Description
The fuzzer consists of 3 main components:
1. Harness -> Execute payloads on each binary and determine if this results in interesting behaviour (errors/crashes/new code)
2. Parser  -> Facilitate the input mutation process by ensuring that file format is maintained and a valid input is given
3. Mutator -> Perform various mutation strategies on the sample input to seed interesting behaviour

Our fuzzer uses various mutation strategies:
- Bit flipping
    - Change arbitrary bits within the sample program input
- Byte flipping
    - Change arbitrary bytes within the input
- Magic values
    - Try long strings, short strings, MAX_INT, MIN_INT, 0xFFFFFFFF etc.
- Format-string fuzzing
    - Try format string specifiers to check for format string vulnerabilities

The harness locates the provided binaries and associated inputs, and depending on the input file type, it will send it to the appropriate parser which strips out modifiable values so they can get mutated. The mutated binary is then provided back to the harness which runs the binary and feeds it the input, monitoring for errors. [add more detail about what kind of errors and how]

The fuzzer can find format string vulnerabilities, buffer overflow vulnerabilities and also detect any mistakes with input parsing, such as making assumptions about the input provided. Testing magic values also acts as boundary testing to make sure edge cases are dealt with appropriately.

Currently, the fuzzer doesn't adapt its strategy depending on the binary or output of already run inputs, so it is "dumb". It also doesn't look for any additional branches in input which might allows more vectors for exploitation. 