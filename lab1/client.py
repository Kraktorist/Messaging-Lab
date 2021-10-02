#!/usr/bin/env python
import pika
import uuid

class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=False)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(on_message_callback=self.on_response, auto_ack=False,
                                   queue=self.callback_queue)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response.decode('utf-8'))

rpc = RpcClient()
arg = str(uuid.uuid4())
print(f" [x] Requesting arg {arg}")
response = rpc.call(arg)
print(f" [.] Got {response}")