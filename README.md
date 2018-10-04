# Flask Celery SocketIO Demo

A demo using flask socketio in celery task.

## Install

1. Install RabbitMQ
2. `pipenv install`

```
# Windows don't support celery 4+, so install celery==3.1.25
pipenv install flask flask_socketio celery==3.1.25
```

## Start Run

```
# console 1: start celery worker
celery worker -A celery_app.celery --loglevel=info

# console 2: start flask app
python flask_app.py

# (optional) consloe 3: start celery flower
celery flower -A celery_app.celery --address=127.0.0.1 --port=5555
```
