# Research CELERY for background tasks and demo

1. Setup Celery in the project:
- Create docker-compose.yaml with needed images – django (Python) image, Celery worker image, Redis image (other message brokers also can be used)

- For Django project configuration of Docker file is:
	
    	FROM python:3.12-slim-bullseye
    
    	WORKDIR /polls_app
    
    	ENV VIRTUAL_ENV=/opt/venv
    
    	RUN python3 -m venv $VIRTUAL_ENV
    
    	ENV PATH="$VIRTUAL_ENV/bin:$PATH"
    
    	COPY requirements.txt .
    
    	RUN pip install -r requirements.txt
    
    	COPY . .

This run docker container with our project in virtual environment. Venv in this case provide additional layer of isolation of the project from the environment.

- App configuration in docker-compose.yaml:

      django:
        build: ./
        container_name: celery_demo
        ports:
          - "8000:8001"
        command: ["/opt/venv/bin/python", "manage.py", "runserver", 	"0.0.0.0:8000"]
        volumes:
          - ./:/celery_demo
        env_file:
          - ./env/django.env
        stdin_open: true
        tty: true
        depends_on:
          - redis

- For Redis in developer environment password may not be set, but in production Redis should have password set, if no password is set in production everyone can access Redis and that raise security concerns. How to set and utilize password????. Configuration of the image is simple:

      redis:
        image: redis:7-alpine
        container_name: redis
  
- Celery image is deprecated and Python image should be used. To created Celery worker in docker container we use code base of our project, so mostly the configuration of worker is same as configuration of django project.

      celery:
        build: ./
        container_name: celery_worker
        command: celery --app=celery_demo worker -l INFO --concurrency=2
        volumes:
          - ./:/celery_demo
        env_file:
          - ./env/django.env
        depends_on:
          - redis

- Set up of settings.py in the project:
	
    	CELERY_BROKER_URL = "redis://redis:6379/0"
    	CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    	CELERY_ACCEPT_CONTENT = ['json']
    	CELERY_TASK_SERIALIZER = 'json'
    	CELERY_RESULT_SERIALIZER = 'json'
    	CELERY_TIMEZONE = 'UTC'





 

