import os
from RabbitMQCommon import Rabbit as Rb
import RabbitMQSend
import random

sqlite_db_name = 'chinook.db'
sqlite_db_path = os.path.join(os.getcwd(),sqlite_db_name)
query_file_name = 'Queries.sql'
print('-- start --')
query_file_path = os.path.join(os.getcwd(), query_file_name)
print('reading query file..')
with open(query_file_path, 'r') as query_file_name:
    lines = query_file_name.read()
    query_file_name.close()
queries_list = lines.split(';\n')

# generate requests
rand_req = random.randrange(10)
print('will create ' + str(rand_req) + ' requests:')
rand_matrix = []
for r_t in range(rand_req-1):
    rand_matrix.append([random.randrange(0, len(queries_list)), random.randrange(0, len(Rb.FORMATS_LIST))])

# send requests
for i, r_id in enumerate(rand_matrix):
    query_id = r_id[0]
    f_type = Rb.FORMATS_LIST[r_id[1]]
    f_name = 'test_'+str(i+1)+'_q'+str(query_id)
    query = queries_list[query_id-1]
    if f_type != 'TABLE':
        f_path = os.path.join(os.getcwd(), 'tests', f_name+'.'+f_type.lower())
    else:
        f_path = f_name

    print('-'*10)
    print('Type:' + f_type)
    print('Path:' + f_path)
    RabbitMQSend.send_request(format_type=f_type,
                              path=f_path,
                              query=query,
                              conn_path=sqlite_db_path
                              )
print('-- end --')
