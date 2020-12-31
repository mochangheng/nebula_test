# Nebula API Test

## How to run this code?

1. Create a virtual Python environment with Python 3.9 (you can use conda, virtualenv, ...).
2. Install the required dependencies by running 

    ```bash
    pip install -r requirements.txt
    ```
3. Install and run a MySQL database server on localhost. More instructions on how to do so [here](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/).
4. If this is the first time you are running this, you need to run `python backend/create_db.py` to set up the database and the table used by the API.
5. Go into the backend directory and start the API. The server logs will be stored in backend/log.csv.
   ```bash
   cd backend/
   bash start_api.sh
   ```
6. You can test the API by running `python test_api.py`. The reported data will be stored in report_data.txt.