import os
import pika
import time

RABBITMQ_HOST = os.getenv('WORKER_RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE = os.getenv('WORKER_QUEUE_NAME')
RABBITMQ_ROUTING_KEY = os.getenv('WORKER_ROUTING_KEY')

SLEEPTIME = 10
print(' [*] Sleeping for ', SLEEPTIME, ' seconds.')
time.sleep(30)

print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

print(' [*] Waiting for messages.')

def callback(ch, method, properties, body):
    print(" [x] Received a message")
    body = body.decode()
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=RABBITMQ_ROUTING_KEY, on_message_callback=callback)
channel.start_consuming()
