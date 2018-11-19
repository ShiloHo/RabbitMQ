#!/usr/bin/env python
import pika
import json


def send_request(format_type, path, query, conn_path, rabbit_host='localhost'):

    """Sending request to RabbitMQ.
    the queue will be 'REQ'.
    the massage contain json line of the request : {'Type': 'JSON', 'Path': '/json_path/', 'Query': 'q1'}.
    """
    request_json_line = json.dumps({'Type': format_type, 'Path': path, 'Query': query, 'Connection Path': conn_path})
    with pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='REQ')
        channel.basic_publish(exchange='',
                              routing_key='REQ',
                              body=request_json_line)
        print("[+] Sent request REQ-%r" % format_type)
        connection.close()
