# consume.py
import pika, os
import requests
import json
import time
# TODO 
# ADDING CONTROLLED STARTUP CONDITION
# READ https://docs.docker.com/compose/startup-order/

backend_url = os.environ.get('BACKEND_URL')


# Callback function - Executes for each message we consumes
def callback(ch, method, properties, body):
  print(" [x] Received %r" % body,flush=True)
  my_json = json.loads(body.decode('utf8'))
  print(my_json,flush=True)
  try:
  	requests.post(backend_url, json=my_json)
  except Exception as e:
  	print(e,flush=True)

# Run rabbitmq consumer
if __name__ == '__main__':
    print(' [*] RabbitMQ consumer: Waiting for messages:')
    while(True):
        try:
            url = os.environ.get('rabbitmq')
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.basic_consume(callback,
                                  queue='helge-api-posts',
                                  no_ack=True)
            try:
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                connection.close()
                break
        except pika.exceptions.ConnectionClosed:
            continue
        except pika.exceptions.AMQPConnectionError:
            continue
