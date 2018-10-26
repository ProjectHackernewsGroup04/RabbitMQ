FROM python:3.6
ADD . /rabbitmq
WORKDIR /rabbitmq
RUN pip install -r requirements.txt
CMD python3 app/rabbitmq_consumer.py
