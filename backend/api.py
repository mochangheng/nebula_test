import os
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import mysql.connector

LOG_FILENAME = 'log.csv'
USE_DB = True
with open('config.json') as f:
    config = json.load(f)

app = FastAPI()
worker_status = {
    1: {
        'worker_name': 'host1',
        'cpu_usage': 0.23,
        'gpu_usage': 0.8,
        'ram_usage': 0.6,
        'gpu_name': 'GeForce RTX 2080',
    },
    2: {
        'worker_name': 'host2',
        'cpu_usage': 0.9,
        'ram_usage': 0.8,
    },
    3: {
        'worker_name': 'host3',
        'cpu_usage': 0.7,
        'gpu_usage': 0.8,
        'ram_usage': 0.8,
        'gpu_name': 'GeForce Titan RTX',
    },
    4: {
        'worker_name': 'host4',
        'cpu_usage': 0.1,
        'gpu_usage': 0.,
        'ram_usage': 0.3,
        'gpu_name': 'GeForce GTX 1080 Ti',
    },
    5: {
        'worker_name': 'host5',
        'cpu_usage': 0.3,
        'ram_usage': 0.4,
    },
    6: {
        'worker_name': 'host6',
        'cpu_usage': 0.7,
        'ram_usage': 0.55,
    }
}

# Set up CSV logging
if os.path.isfile(LOG_FILENAME):
    log_file = open(LOG_FILENAME, 'a')
else:
    log_file = open(LOG_FILENAME, 'a')
    log_file.write(',API_CALL_DATA,API_KEY,API_VALUE\n')
    log_file.flush()

def save2csv(call_data, key, value):
    log_file.write(f"{call_data},{key},{value}\n")
    log_file.flush()

# Set up storing to DB
if USE_DB:
    try:
        connection = mysql.connector.connect(
            host=config['db_host'],
            user=config['db_user'],
            password=config['db_password'],
            db="nebula",
        )
    except:
        print("WARNING: Cannot connect to database. Data will not be stored to database..")
        USE_DB = False

def save2db(call_datetime, success):
    if not USE_DB:
        return

    error_counts = 0 if success else 1
    with connection.cursor() as cursor:
        sql = "INSERT INTO api_calls (admin_id, call_date, call_time, result, error_counts) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, ('admin_1', call_datetime.date(), call_datetime.time(), success, error_counts))

    connection.commit()

# Set up authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
valid_tokens = ['43jE2ID93jxP92']

def verify_token(token):
    return token in valid_tokens

@app.get('/workers/')
async def get_worker_status(worker_id: int, token: str = Depends(oauth2_scheme)):
    time = datetime.now()
    exception = None

    if not verify_token(token):
        exception = HTTPException(status_code=401, detail='Invalid token.')
    elif not (worker_id >= 1 and worker_id <= 6):
        exception = HTTPException(status_code=404, detail='Worker not found.')
    else:
        response = worker_status[worker_id]
        response['worker_id'] = worker_id

    if exception is not None:
        save2db(time, False)
        raise exception
    else:
        save2csv(worker_id, token, response['worker_name'])
        save2db(time, True)
        return response