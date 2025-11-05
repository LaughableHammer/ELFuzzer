### Fuzzer plan
Imo there's 3 main aspects to the fuzzer:
- The harness will efficiently execute payloads and determine if they produce interesting behaviour and should be further explored
- The file format parser/encoder will determine what we should change about the format and ensure we focus on valid input formats
- The mutator will use strategies to change the input slightly to try to find a vulnerability, such as by inserting format strings or flipping some bits

Aspects of fuzzer to program:
- Payload generation:
	- We should solve the provided binaries to understand the types of mutations to the input we should program
	- We are provided a list of mutation strategies to implement:
		- Bit flips
		- Byte flips
		- Known ints
			- Eg format strings
		- Repeated parts
		- Keyword extraction
		- Arithmetic
		- Coverage based
- File format parser/encoder
	- I think someone who is good at swe design (like 2511 stuff) should spend a while researching each of the formats and the provided binaries to think of a nice way to reduce duplicated code.
	- It should be easy to actually code up the parsers/re-encoders once we come up with a good design and have stubs to fill out.
	- Imo this design should be peer checked before implementation.
- Harness:
	- Needs to be performant, if someone is interested in low level stuff with memory and potentially interfacing with C using ctypes this would be helpful.
		- Multithreading??? Depends how server/docker is setup ig
	- Coverage testing is probs hardest part of assignment imo where we use ptrace/ltrace/stdout to determine if inputs are interested and should be further developed - eg if the binary is locked behind a 4 digit pin we should focus on payloads that use the pin.

Other parts of project:
- Finding all vulnerabilities in all 11 binaries
- Creating test vulnerable binaries
- Useful statistics/output
- Creating concise writeup

(I'm working on this in obsidian, lmk if people prefer smth like Google Docs)
