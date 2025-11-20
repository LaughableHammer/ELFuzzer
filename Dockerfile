FROM python:latest
 
COPY colours.py /
COPY mutators /mutators
COPY created_binaries /created_binaries
COPY harness.py /
COPY parser.py /
COPY fuzzer.py /
COPY globalVar.py /
COPY agnostic_mutator.py /
COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install --root-user-action -r requirements.txt
CMD ["python", "fuzzer.py"]
