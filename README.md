# WaitList-App-Backend
## Requirements :
- Python Version:  3.10.6 or higher.
- CPython version : 3.10.6 or higher
- Pip version : 22.0.2 or higher
- Uvicorn : 0.15.0 or higher
- MySQL database
- Postman to test the api endpoints

## Project setup : 
1. Setup this repo locally
1. Apply `ddl.txt` on MySQL
2. `pip -r requirements.txt`
3. Setup email connection in `config.json` [ to check the send email feature only ]
4. Edit database connection details in `config.json`

## Run project :
1. If you're using linux , run `sudo chmod +x ./app.sh` and `./app.sh`
2. If you're using windows , run `uvicorn main:app`

## To view all the available endpoints :
- set `listAPI` to true in `config.json`
- start the application
- search `host:port/docs` [ example : http://127.0.0.1:8000/docs ]
