# REST API With Flask & SQL Alchemy

> Products API using Python Flask, SQL Alchemy and Marshmallow

# Install REST extension in your Virsual Studio Code
You can test api in request.rest file in Virsual Studio Code

## Quick Start Using Pipenv

``` bash
# Install pipenv
$ pip3 install pipenv

# Activate venv
$ pipenv shell

# Install dependencies in Pipfile
# if there is no Pipfile, you can install manully :
# $ pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
# if your project dependencies file is requirements.txt, you can use this :
# $ pipenv install -r /path/to/your/requirements.txt
$ pipenv install

# Create DB
# enter python shell in your venv
$ python
>> from app import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /product
* GET     /product/:id
* POST    /product
* PUT     /product/:id
* DELETE  /product/:id