from flock.app import app
from flock.services import mail
from flock.services import notification

def start_celery_worker():
    from celery import current_app
    from celery.bin import worker

    celery_app = current_app._get_current_object()
    worker = worker.worker(app=celery_app)
    options = {
        'broker': app.config['CELERY_BROKER_URL'],
        'loglevel': 'INFO',
        'traceback': True
    }
    worker.run(**options)

if __name__ == '__main__':
    start_celery_worker()