#!/usr/bin/env python
import json
import xml.etree.ElementTree as xmlElementTree
import csv
import sqlite3
"""common functions, class."""

class Rabbit:

    """ global params"""
    FORMATS_LIST = ('JSON', 'CSV', 'XML', 'TABLE')
    CREATE_TABLE_STRING_LIST = ('CREATE TABLE ', ' AS ')

    class Request:

            def __init__(self, type, path, query,connection_path):
                self.type = type.upper()
                self.path = path
                self.query = query
                self.connection_path = connection_path

    def SqliteDBExecute(request):
            """will connect to sqlite3 DB and run request query.
             in case of TABLE request type it will create it immediately."""
            with sqlite3.connect(request.connection_path) as connection_sqlite:
                cursor_sqlite = connection_sqlite.cursor()
                export_data = ""
                header_columns = ""
                if request.type == 'TABLE':
                    try:
                        cursor_sqlite.execute(request.path.join(Rabbit.CREATE_TABLE_STRING_LIST) + request.query)
                    except sqlite3.OperationalError as e:
                        print('Sqlite operational error: {}'.format(e))
                elif request.type in Rabbit.FORMATS_LIST:
                    try:
                        data_exec = cursor_sqlite.execute(request.query)
                        export_data = data_exec.fetchall()
                        header_columns = [column[0] for column in data_exec.description]
                    except sqlite3.OperationalError as e:
                        print('Sqlite operational error: {}'.format(e))
                return export_data, header_columns
    class Files:

        def CreateXML(path,data,header):
            """handling XML file type."""
            xml_data = xmlElementTree.Element('data')
            rows = xmlElementTree.SubElement(xml_data, 'rows')
            for row in data:
                xml_row = xmlElementTree.SubElement(rows, 'row')
                for position, col in enumerate(header):
                    column = xmlElementTree.SubElement(xml_row, col)
                    column.text = str(row[position])

            with open(path, 'wb') as xml_file:
                str_data = xmlElementTree.tostring(xml_data, encoding='utf8', method='xml')
                xml_file.write(str_data)

        def CreateJSON(path,data,header):
            """handling JSON file type."""
            json_rows = []
            for row in data:
                row_dict = {}
                for position, col in enumerate(header):
                    row_dict[col] = row[position]
                json_rows.append(row_dict)
            with open(path, 'w') as json_file:
                json.dump(json_rows, json_file)

            with open(path, 'w') as json_file:
                 json.dump(data, json_file)

        def CreateCSV(path,data,header):
            """handling CSV file type."""
            with open(path, 'w', encoding='utf8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)
                writer.writerows(data)

        def SwitchType(type,path,data,header):
            try:
                if type == 'CSV':
                    Rabbit.Files.CreateCSV(path, data, header)
                if type == 'JSON':
                    Rabbit.Files.CreateJSON(path, data, header)
                if type == 'XML':
                    Rabbit.Files.CreateXML(path, data, header)
                print("  - File %rs created." % path)
            except FileNotFoundError as e:
                print('File Not Found Error: {}'.format(e))


