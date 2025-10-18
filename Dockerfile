FROM python:3.9-slim-bookworm

COPY fileformat.py /
COPY harness.py /
COPY mutator.py /

CMD ["python", "-i", "harness.py"]
