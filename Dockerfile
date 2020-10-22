FROM python:3.7.9-slim

ADD ./requirements.txt .
RUN python -m pip install -r requirements.txt

ADD ./embedding ./embedding

ENTRYPOINT ["python", "/embedding/main/main.py"]

