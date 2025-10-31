FROM python:latest

COPY colours.py /
COPY harness.py /
COPY json_csv_mutator.py /
COPY plaintext_mutator.py /

CMD ["python", "-i", "harness.py"]
