# RabbitMQ

1. sending requests to RabbitMQ.

2.connect to sqlite3 DB and run request query that recieved from RabbitMQ.
 in case of TABLE request type it will create it immediately.
 handling CSV, JSON, XML file type.



Modules:

RabbitMQCommon
 common functions, class.
RabbitMQSend :
 This module get a JSON line and send it to RabbitMQ.

RabbitMQReceive:
 This module receive  requests from RabbitMQ and execute all.

Tests scripts:

*test_send_multi_requests.py:
  Script for creating random requests and send it to RabbitMQ.

*test_recived_all.py:
  Receive and execute all requests from RabbitMQ.

*test_send_recive_wrong.py:
 Script for testing wrong requests send and received.

*test_clean.py:
 Script for cleaning test files and tables


