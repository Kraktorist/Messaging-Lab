from json import dumps
from flask import Flask, request
import os
import pika



app = Flask(__name__)
app.rabbitmq_host = os.getenv('WEBHOOK_RABBITMQ_HOST', 'localhost')
app.rabbitmq_queue = os.getenv('WEBHOOK_QUEUE_NAME')
app.rabbitmq_routing_key = os.getenv('WEBHOOK_ROUTING_KEY')
app.app_ip = os.getenv('WEBHOOK_IP', '0.0.0.0')
app.app_port = os.getenv('WEBHOOK_PORT', 5000)


@app.route('/')
def index():
    return 'OK'


@app.route('/alert', methods=['POST'])
def alert():
    """Create an alert"""
    message = request.get_json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=app.rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=app.rabbitmq_queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=app.rabbitmq_routing_key,
        body=dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, host=app.app_ip, port=app.app_port)
    