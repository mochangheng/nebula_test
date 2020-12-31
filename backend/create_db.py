import json

import mysql.connector

with open('config.json') as f:
    config = json.load(f)

connection = mysql.connector.connect(
  host=config['db_host'],
  user=config['db_user'],
  password=config['db_password']
)
cursor = connection.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS nebula;')
cursor.execute('USE nebula;')
query = '''
    CREATE TABLE IF NOT EXISTS api_calls (
        call_id INT AUTO_INCREMENT PRIMARY KEY,
        admin_id VARCHAR(255) NOT NULL,
        call_date DATE,
        call_time TIME,
        result TINYINT,
        error_counts INT
    );
'''
cursor.execute(query)
cursor.close()
connection.close()