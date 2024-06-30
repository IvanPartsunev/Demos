# Research CELERY for background tasks and demo

Setup Celery in the project:
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
        command: celery --app=celery_demo worker -l INFO
        volumes:
          - ./:/celery_demo
        env_file:
          - ./env/django.env
        depends_on:
          - redis

- Celery image is deprecated and Python image should be used. To created Celery worker in docker container we use code base of our project, so mostly the configuration of worker is same as configuration of django project.
      
      import os
      from celery import Celery

      os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_demo.settings")
      app = Celery("celery_demo")

      app.config_from_object("django.conf:settings", namespace="CELERY")

      app.conf.update(
        worker_concurrency=2,
      )

      app.conf.task_routes = {"celery_demo.tasks.*": {"queue": "celery_demo_q_1"}}
      app.autodiscover_tasks()


  
- Set up of settings.py in the project:
	
    	CELERY_BROKER_URL = "redis://redis:6379/0"
    	CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    	CELERY_ACCEPT_CONTENT = ["json"]
    	CELERY_TASK_SERIALIZER = "json"
    	CELERY_RESULT_SERIALIZER = "json"
    	CELERY_TIMEZONE = "UTC"

- celery.py:


         from celery import Celery
    
         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_demo.settings")
    
         app = Celery("celery_demo")
         app.config_from_object("django.conf:settings", namespace="CELERY")
    
         app.conf.update(
            worker_concurrency=2,
         )
    
         app.conf.task_routes = {"celery_demo.tasks.*": {"queue": "celery_demo_q_1"}}
    
    
         app.autodiscover_tasks()


- Celery workers can have queues for their tasks, tasks can have priority levels.
- Celery tasks can be grouped or chained. Difference is that when they are grouped, grouped tasks will be executed randomly. When chained tasks will be executed in specific order we determine. What is dow mostly when tasks have dependencies between them and for example task2 need the result of task 1.

- Celery workers can be scaled depends on load. Most of the server providers offer automatic scaling.



# Research methods of fetching data from client ERP (from API)

- set up Redis as project CACHE (settings.py):

      CACHES = {
          "default": {
              "BACKEND": "django_redis.cache.RedisCache",
              "LOCATION": "redis://redis:6379/1",  # Use a different Redis database to separate cache from Celery broker
              "OPTIONS": {
                  "CLIENT_CLASS": "django_redis.client.DefaultClient",
              }
          }
      }
  Here we use "redis://redis:6379/1" because we run the project in Dockerized environment. In local environment "localhost" should be used.

- set up Celery beat to schedule API calls (settings.py):

      from celery.schedules import crontab

      <other settings>

      CELERY_BEAT_SCHEDULE = {
          "fetch-and-cache-data-every-minute": {
              "task": "celery_demo.tasks.<scheduled_task>",
              "schedule": crontab(minute="*"),  # Run every minute
              # "schedule": crontab(minute="0", hour="0,12"),  # At midnight and noon
          },
      }
- 
