# HealthCompanion


## Description

## How to run the application

To run the server you need to install the dependencies

```bash
pip install -r requirements.txt
```

or with a virtual environment

```bash
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt
```

Then you can run the server with

Windows : 
```bash
cd app
py run.py
```

Linux/ Mac : 
```bash
cd app
python3 run.py
```

To run the db

```bash
docker run --rm -t -i -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password couchdb:3.3.3 --name couchdbCompanion
```