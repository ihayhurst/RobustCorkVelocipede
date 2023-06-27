# Readme

## About the project
An API using fastapi to transform endpoints from a database ( This was Vertica, could easily be Oracle etc.) for consumption in Optibrium 's deep-learning drug discovery tool  https://optibrium.com/cerella/ Cerella.

## This code:
by Ian M. Hayhurst. 
- Uses the uvicorn-gunicorn  fastapi docker image tiangolo/uvicorn-gunicorn-fastapi:python3.11 https://github.com/tiangolo/uvicorn-gunicorn-docker provided by fastapi author (Sebastián Ramírez). 
- Includes units.py from Optibriums's Stardrop

## Procedure
- Create a config.ini file containing your database credentials and store it in the /app folder
build and start the image
`docker build -t fastapi .`
- In a development environment it's helpful to mount your app folder into the container and use the start-reload.sh  so changes are reflected immediatly without lots of rebuilding and restarting
`docker run -d -p 80:80 -v $(pwd):/app fastapi /start-reload.sh`

- For 'Production' 

`docker run -d --name fastapi -p 80:80 fastapi`

## Example of config.ini required to supply the Database credentials (not included here)
```
[DATABASE]
HOST = Vbiodata001.something.eu-central-1.rds.amazonaws.com
NAME = BIODATA1
PORT = 5433
USER = my_user
PASWSWORD = my_password
```
