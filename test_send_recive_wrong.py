import os
from RabbitMQRecive import get_request
import RabbitMQSend
""" Receive and execute all requests from RabbitMQ."""

sqlite_db_name = 'chinook.db'
sqlite_db_name_w = 'chino1.db'
sqlite_db_path = os.path.join(os.getcwd(),sqlite_db_name)
sqlite_db_path_w = os.path.join(os.getcwd(),sqlite_db_name_w)
q_w_table = 'SELECT * FROM TABLE_NOT_EXISTS;'
query_file_name = 'Queries.sql'


print('-- start --')
query_file_path = os.path.join(os.getcwd(), query_file_name)
print('reading query file..')
with open(query_file_path, 'r') as query_file_name:
    lines = query_file_name.read()
    query_file_name.close()
queries_list = lines.split(';\n')

RabbitMQSend.send_request(format_type='TABLE',
                          path= 'test_wrong_type_1',
                          query=queries_list[1],
                          conn_path=sqlite_db_path
                          )

# test wrong file type

RabbitMQSend.send_request(format_type='EXCEL',
                          path=os.path.join(os.getcwd(), 'tests', 'test_wrong_type_1.excel'),
                          query=queries_list[1],
                          conn_path=sqlite_db_path
                          )
# test wrong db

print(sqlite_db_path_w)
RabbitMQSend.send_request(format_type='CSV',
                          path=os.path.join(os.getcwd(), 'tests', 'test_wrong_db.csv'),
                          query=queries_list[0],
                          conn_path=sqlite_db_path_w
                          )
# test wrong query - table

RabbitMQSend.send_request(format_type='CSV',
                          path=os.path.join(os.getcwd(), 'tests', 'test_wrong_query.csv'),
                          query=q_w_table,
                          conn_path=sqlite_db_path
                          )

get_request(rabbit_host='localhost')


print('-- end --')