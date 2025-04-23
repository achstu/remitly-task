# SWIFT Codes API

A REST API for managing and querying SWIFT.

## Technology Stack

- **Language**: Python (FastAPI)
- **Database**: SQLite (with Peewee ORM)




## Setup Instructions

For minimal setup just create python virtual environment and install dependencies listed in [requirements.txt](./requirements.txt). After that run

```bash
python create_db.py
```

This script creates SQLite `banks.db` database from provided spreadsheet (previuosly downloaded from [here](https://docs.google.com/spreadsheets/d/1iFFqsu_xruvVKzXAadAAlDBpIuU51v-pfIEU5HeGa8w/edit?gid=0#gid=0)). Then you can just start server via entering

```bash
uvicorn main:app --port 8080
```

## API Endpoints

Too see comprehensive docs navigate to http://localhost:8080/docs.
