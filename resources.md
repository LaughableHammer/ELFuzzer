# Mutation Strategies 
Fuzzing should always take valid input and then tweak it. Especially when dealing with magic bytes. 
Take a valid (seed) inputs, and tweaks it:
- additive fuzzer: takes a small input and slowly builds it up

# Considerations
- Use magic bytes to identify the file that is being parsed and adjust accordingly
- Saving memory states? 
- Hanging programs? 
- GENETIC FUZZING WOOHOO
# Resources and Notes
- [Building a simple coverage based fuzzer for binary code | xct's blog](https://vuln.dev/building-a-simple-coverage-based-fuzzer-for-binary-code/)
- [What is Fuzz Testing? A Thorough Guide with Code Examples – TheLinuxCode](https://thelinuxcode.com/what-is-fuzz-testing-a-thorough-guide-with-code-examples/)
- [secfigo/Awesome-Fuzzing: A curated list of fuzzing resources ( Books, courses - free and paid, videos, tools, tutorials and vulnerable applications to practice on ) for learning Fuzzing and initial phases of Exploit Development like root cause analysis.](https://github.com/secfigo/Awesome-Fuzzing)
- [Build a fuzzer  |  Fuchsia](https://fuchsia.dev/fuchsia-src/development/testing/fuzzing/build-a-fuzzer)
- https://fuchsia.dev/fuchsia-src/development/testing/fuzzing/write-a-fuzzer
- [libFuzzer – a library for coverage-guided fuzz testing. — LLVM 22.0.0git documentation](https://llvm.org/docs/LibFuzzer.html)

- https://www.offsec.com/metasploit-unleashed/writing-simple-fuzzer/

- https://carstein.github.io/fuzzing/2020/04/18/writing-simple-fuzzer-1.html
	- https://lobste.rs/s/5kno0l/build_simple_fuzzer_part_1 (corrections of the original author)
- https://h0mbre.github.io/Fuzzing-Like-A-Caveman/#
- https://h0mbre.github.io/Fuzzing-Like-a-Caveman-2/
- https://h0mbre.github.io/New_Fuzzer_Project/

## Hacking Livestream: Fuzzing
- https://www.youtube.com/watch?v=BrDujogxYSk (#17 Basics of Fuzzing, and codes up a random fuzzer as well)
	- Easiest is just to pick a byte and change it. 
	- Attach a debugger and obtain a report. 
	- Ideally find one main area and focus on it. Otherwise it is going to be slow.
	- Corpus: input samples
	- Bitflips/byteflips: usually take a percentage of the number of bytes (e.g. 1%)
	- Mutator that finds and changes number
	- Moving chunks of the data
	- Appending to the end
	- Can attach GDB with script to check output, and can detect if SEGFUALT. He also has some interesting gdb techniques. 1:17. Debugger is slower though. 
- https://www.youtube.com/watch?v=JhsHGms_7JQ (Genetic Fuzzing Theory)
- https://www.youtube.com/watch?v=HN_tI601jNU (Genetic Fuzzing Implementation)
## Gamozolab
- https://www.youtube.com/watch?v=SngK4W4tVc0 (Adventures in Fuzzing, apparently has crazy harness strategies)
- https://www.youtube.com/watch?v=947b0lgyvJs (How to minimize the Corpus)
	- Keeping the smallest set that generates all the inputs **Question: how do I measure coverage? And how do I minimize corpus?**
	- Might not help -- consider overall. Might favour the input. Moose example is a con. 
	- A significant number of cases are dependent on previous states. Minimizing might cause significant states that get lost.
	- Partial solution to a problem called input bloat. 
	- it is still widely used in commercial. 
	- The larger the program, the slower to fuzz. Consider corpus. So minimization depends on the speed. 
	- Try it -- see if it is effective. Just see how each input is fuzzed. Figure if it is a good program or not. Find a different metric to track as a method. 50% 50% on a non minimized and minimized corpus. Random strategy of picking a strategy.


- https://srlabs.de/blog/guide-to-writing-fuzzing-harness
## Trail of Bits
Playlist: [Learn how to fuzz like a pro: Introduction to fuzzing](https://www.youtube.com/watch?v=QofNQxW_K08&list=PLciHOL_J7Iwqdja9UH4ZzE8dP1IxtsBXI)
- https://www.youtube.com/watch?v=9P7sqE6hILM (Fuzzing Arithmetic)
- https://www.youtube.com/watch?v=QofNQxW_K08 (Introduction to Fuzzing)
## Genetic Fuzzing
- https://download.vusec.net/papers/ifuzzer-esorics16.pdf
- https://www.imperva.com/learn/application-security/fuzzing-fuzz-testing/#:~:text=Evolution%20Fuzzers&text=Genetic%20algorithms%20use%20the%20concepts,continuous%20set%20of%20test%20cases.
- https://coalfire.com/the-coalfire-blog/fuzzing-common-tools-and-techniques
- https://aflplus.plus/docs/afl-fuzz_approach/
- https://www.fuzzingbook.org/html/MutationFuzzer.html (THIS LOOKS COOL)
- https://www.coderskitchen.com/fuzzing-techniques/
- https://www.jaybosamiya.com/blog/2017/05/27/genetic-fuzzing/