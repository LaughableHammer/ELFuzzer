FROM python:latest

# TODO: pip install pyelftools

COPY colours.py /
COPY harness.py /
COPY json_csv_mutator.py /
COPY plaintext_mutator.py /

CMD ["python", "fuzzer.py"]
