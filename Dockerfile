FROM python:3.7.9-slim

ADD ./requirements.txt .
RUN python -m pip install -r requirements.txt

ADD ./embedding ./embedding

ADD ./cc.pt.300.vec ./cc.pt.300.vec

EXPOSE 8098

ENTRYPOINT ["python", "/embedding/main/main.py"]

