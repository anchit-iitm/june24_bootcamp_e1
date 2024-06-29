from celery import Task
from app import create_app

app, _, _ = create_app()

class taskContext(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs) 