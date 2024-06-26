# HealthCompanion
If you want to try to use HealthCompanion using a:
* doctor profile, you can log in using the following identifiers:
    * *email:* doc.jean.eude@gmail.com
    * *password:* password
* patient profile, you can log in using the following identifiers:
    * *email:* jean.dupont@gmail.com
    * *password:* password

## Description

HealthCompanion is a web application that allows users to track their vaccine history and schedule their next vaccine.

## How to run the application
### Using the makefile
Launch the docker that manages the db
```bash
make start
```

Launch the application
```bash
make app
```

Kill the docker 
```bash
make clean
```

### Using command lines

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

## API reference

The API is documented in the swagger file `static/swagger.json`. 

### Using default swagger visualization
To view the documentation, run the server and go to [/swagger](http://localhost:5000/swagger).

### Using Orthanc design
Use these commands to launch a server:
```sh
cd OpenAPI
python3 -m http.server 8000
```

Now you can consult the documentation at this address: http://localhost:8000/