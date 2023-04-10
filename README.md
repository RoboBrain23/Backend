# RoboBrain (In Progress)

## Description

This Repository contains the Backend code that have been used in RoboBrain Project.

## Content

### Routes

The repository contains the following routes:
| METHOD | ROUTE | FUNCTIONALITY | ACCESS |
| ----------- | ----------- | ----------- | ---------|  
| ***POST*** | /chair/data | Store the upcoming sensor's data | *Superusers* |
| ***GET*** | /chair/data | Get sensor's data | *Superusers* |
| ***POST*** | /patient/signup | Register new user | *All users* |
| ***POST*** | /patient/login | Login user | *All users* |
| ***GET*** | /patient/me | Get patient information | *Superusers* |

### Files

The repository contains the follwoing files:

- `main.py`
: The main file that combine all the routes together and run the server with
- `test_main.py`
: Where we test our routes from sending correct and wrong requests and shows the expected response
- `requirements.txt`
: Contains all the packages and dependencies needed 
- `routers/chair.py`
: Contains all the routes related to the data that will come from chair's sensors
- `routers/patient.py`
: Contains all the routers related to the patient that will use the mobile app and the chair
- `db/database.py`
: Where we connect to our PostgreSQL database
- `db/models.py`
: Contains the models that will create our tables in database
- `db/crud.py`
: Contains all the needed function to process the CRUD operations for the routes
- `db/schemas.py`
: Contains all the schemas that used in Request and Response operations
- `auth/schema.py`
: Contains the configuration settings for JWT and the schema used in returning the access token


## Prerequisite

All needed Packages and libraries included in `requirements.txt` you can install it by following the instructions: 

### Create Virtual environment

```
python -m venv venv
```

### Activate the Virtial environment

_For Git Bash_
``` 
source venv\Scripts\activate
```

_For Powershell or cmd_
```
venv\Scripts\activate
```

### Install requirements
```
pip install requirements.txt
```

## Usage

You can run the server by typing the following command line:
```
uvicorn main:app --reload
```
