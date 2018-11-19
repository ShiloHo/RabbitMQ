#!/usr/bin/env python
import os
import json
import pika
from RabbitMQCommon import Rabbit as Rb


def create_file(request, data, header):
    """Handle files"""
    Rb.Files.SwitchType(request.type, request.path, data, header)


def callback(ch, method, properties, body):
    json_dict = json.loads(body.decode("utf-8"))
    try:
        req = Rb.Request(type=json_dict["Type"],
                         path=json_dict["Path"],
                         query=json_dict["Query"],
                         connection_path = json_dict["Connection Path"]
                         )
        print("[-] Received REQ-Type: %r" % req.type)
        if req.type not in Rb.FORMATS_LIST:
            print("Request type %r is not valid." % req.type)
        else:
            # connect and get the data, in case of table, it will create it.
            [export_data, header_columns] = Rb.SqliteDBExecute(req)
            if req.type != 'TABLE':
                 create_file(req, export_data, header_columns)
    except TypeError as e:
        print('Type Error: {}'.format(e))


def get_request(rabbit_host='localhost'):
    """Receive  requests from RabbitMQ and execute all."""
    with pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue='REQ')
        try:
            channel.basic_consume(callback,
                                  queue='REQ',
                                  no_ack=True)
            print('[*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except KeyboardInterrupt as e:
            print('Keyboard Interrupt: {}'.format(e))
