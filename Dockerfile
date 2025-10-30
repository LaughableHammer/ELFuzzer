FROM python:latest

COPY colours.py /
COPY fileformat.py /
COPY harness.py /
COPY mutator.py /

CMD ["python", "-i", "harness.py"]
