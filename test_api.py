import random
from datetime import datetime
import requests

TOKEN = '43jE2ID93jxP92'
headers = {'Authorization': f'Bearer {TOKEN}'}
r = requests.get('http://127.0.0.1:8000/workers/', params={'worker_id': random.randint(1, 6)}, headers=headers)

if r.status_code >= 200 and r.status_code < 300:
    print('Call successful. The response is stored in report_data.txt')
else:
    print('Call failed. More details in report_data.txt')

with open('report_data.txt', 'a') as f:
    f.write(f"[{datetime.now()}, Status Code {r.status_code}] {r.json()} \n")