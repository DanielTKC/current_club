# current-club

## Team Members

README.md

* Josh C Keller
* Sam R Ramos 02/16/24
* Katie N Cooper
* Daniel I Terreros

# KC CURRENT CLUB HOW TO

1. Head over to and download [Docker](https://docs.docker.com/get-docker/)

2. Using terminal,clone the **main** repository into whatever folder you will be using this command in terminal
- git clone https://github.com/DanielTKC/current_club.git


3. If this is a fresh download of the existing repo type `docker-compose build --no-cache`

## **OR** ##

4. Type `docker-compose up`. This will install current files, dependencies, virtual env, and django. May take a minute.

6. Open a second terminal in visual studio code and follow these steps
- `docker-compose exec app bash` <-This is gives you access to the container's file system
- `poetry shell` <- This takes you to the commandline of the virtual environment
- `cd src` <- Moves you into the django project itself
- `python manage.py migrate` <- Applies any migrations.

[http://127.0.0.1:8000/](http://127.0.0.1:8000/) for index page

[http://127.0.0.1:8000/matches](http://127.0.0.1:8000/matches) to view matches with suite availability 

[http://127.0.0.1:8000/api](http://127.0.0.1:8000/api) for clickable API

## NOW WITH SWAGGER UI AND REDOC ##

[http://127.0.0.1:8000/api/schema/swagger-ui](http://127.0.0.1:8000/api/schema/swagger-ui)

[http://127.0.0.1:8000/api/schema/redoc](http://127.0.0.1:8000/api/schema/redoc)




