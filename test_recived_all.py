#!/usr/bin/env python

from RabbitMQRecive import get_request
""" Receive and execute all requests from RabbitMQ."""
get_request(rabbit_host='localhost')
