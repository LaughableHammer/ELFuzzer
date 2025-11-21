We are submitting this believing that it is not late since give says it is due at 6pm. If you think it is late and would apply the late penalty, please mark Elisa Oda's submission instead.

# Fuzzer Description
ELFuzzer consists of 3 main components:
1. Harness -> Execute payloads on each binary and determine if this results in an interesting behaviour (crash, invalid memory write, heap UF etc.)
2. Parser -> Detects the filetype of the input and then caches this value. This input is then converted to mutateable object depending on the file type.
2. Mutator -> Perform various mutation strategies on the sample input to seed interesting behaviour, with varying techniques for each file type along with a set of common mutators that are shared between each.

## Mutations

Our fuzzer currently uses the following mutation strategies which in most cases are round-robin'd between:
- For plain text -> extend existing input (via duplication), add random bytes to input, bitflips, byteflips, adding format strings randomly and adding magic bytes (-1, MAX_INT etc.) 
- For JSON  -> duplicate a random entry, modify a random entry, add additional depth in a location, add an additional JSON object in a new branch, add a new entry, modify a key randomly, remove entries, and set a value to null.
- For CSV -> mutate a random cell, duplicate some rows
- For XML -> for an xml tree, add nodes to it, remove nodes from it, modify the value of particular nodes, add remove and modify attributes of an xml object, change the tag of a node, change the root, swap the order of two nodes and add additional depth to the xml tree
- For JPEG -> duplicate random parts of the jpeg, modify jpeg marker segment, remove and mutate segments
- For PDF -> changing numbers contained within the file's metadata and mutating text within compressed streams

The shared common mutator library is usually called in some capacity in all of the mutators, providing efficient access to shared mutators.

Almost all of these file mutators utilise a corpus to mutate the sample input, and then perform further mutations on the mutated input itself, allowing for more diverse inputs that vary significantly from the initial sample. This corpus is trimmed when it gets too big and occasionally, the sample input is added back to it to ensure we don't stray too far from the expected format.

## Parser
Our parser design allows for tailored fuzzing of various file types and formats by doing file specific parsing, for example, CSV files are converted into 2D arrays and reconstructed back into CSVs after mutation and XML inputs are parsed into XML trees using libraries.


## Harness
The harness in this fuzzer is responsible for running the binary with the mutated input and monitoring outputs as well as collecting important statistics about the fuzzing process, keeping the user informed during the process by providing an interactive and colourful design. 
During runtime, the harness displays:
- Binary and sample input location
- Total fuzzing attempts (for this binary)
- Fuzzing attempts per second
- First 50 bytes of every other input tested

Crashes are determined by examining the return code of the program, namely when the return code value is less than 0 as this is standard for program crashes. However, we recognised that some binaries may not adhere to these program design paradigms and so we implemented an additional check by matching stderr output to expected output for the particular error (in cases where stderr is populated, such as for stack smashing).
On a crash being detected, parts of the crash-causing input are shown in the terminal, along with total attempts and time it took to cause the crash. For consistency purposes, we set the seed of the random library to the iteration number for each binary, which ensures that random generates the same output each time on the same attempt which improves debugging time and shows changes in fuzzing strategy more clearly.
The harness also keeps the sample input in memory ensuring file reads aren't happening unecessarily and mutated values are generated and used in memory so no files are created or destroyed which would causes unnecessary overhead. In the interest of time spent in total fuzzing, there is also a 3 second timeout on each iteration of the binary, ensuring that significant time isn't wasted on a binary that is running very slow when parsing a particular input.


Additionally, after the fuzzing has ended, the program entrypoint, fuzzer.py generates collective statistics including:
- the number of binaries processed
- how many were successfully crashed
- the total time as well as average program runtime per binary

allowing for tweaking and optimisation of various parameters.

# Bugs we find
The fuzzer is effective at finding overflow-based vulnerabilities in binaries, by spamming very large inputs wherever possible and also via duplication of values within the data structure of the relevant file, whatever the format may be (adding nodes in XML, duplicating lines in CSV etc.).
Additionally, format string vulnerabilities are also detected by adding %s and %n to inputs to cause incorrect dereferencing or writing data to a part of memory which can cause an error/crash. This is highly effective and wherever user input is used as the format string for any relevant function, the vulnerability is usually discovered.

Replacing some values with random ints and magic chars like MIN_INT, MAX_INT, -1, 0xFF etc, we are able to discover incorrect error checking (such as writing past the end of an array) and exploit edge cases that weren't considered by the programmer.

The fuzzer can find bugs with how CSVs and JSON files are parsed, it can look for buffer overflows in text and csv and json files by modifying random values to be very large. It can also detect format string vulnerabilities in plaintext input binaries by placing crash inducing format specifiers randomly in the input.

# Something Awesome
Our something awesome is a web interface for the fuzzer, which provides the ability to submit a binary and an input file which then gets fuzzed by the program. We can customise program parameters such as program runtime and timeout per binary run. 

It then runs the fuzzer on a binary and brings the user to an interface. Flask Event streams will then bring live updates of the fuzizng progress, such as number of attempts, current input and completion status. It also has an ASCII art.

This web interface is completed using Python Flask. It sits on top of the actual fuzzer, with some extra implementation (global variable) to facilitate information transfer between the fuzzer and the web interface. To run the server inside the Docker container execute `./run_fuzzer_server.sh`.




# Improvements 
Current limitations of the fuzzer include
- No multithreading resulting in reduced fuzzing speeds
- lack of coverage based testing resulting in less personalised fuzzing
- Lack of PDF specific fuzzing techniques
- Lack of in-memory resetting which results in reduced fuzzing speeds
