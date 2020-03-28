FROM python:3

RUN mkdir /service
WORKDIR /service
COPY requirements.txt /service/
RUN pip install -r requirements.txt
COPY src/V1/* /service/