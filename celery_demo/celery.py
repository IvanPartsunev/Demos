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


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
