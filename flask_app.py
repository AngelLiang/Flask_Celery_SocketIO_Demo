# coding=utf-8
"""
install:
    pipenv install flask flask_socketio celery==3.1.25

start:
    celery worker -A celery_app.celery --loglevel=info
    python flask_app.py
"""

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.update(
    # Redis
    # CELERY_BROKER_URL='redis://localhost:6379',
    # CELERY_RESULT_BACKEND='redis://localhost:6379',
    # RabbitMQ
    CELERY_BROKER_URL='amqp://guest:guest@localhost:5672//',
    CELERY_RESULT_BACKEND='amqp://guest:guest@localhost:5672//',
)

# 使用 RabbitMQ 存储 SocketIO 的消息队列，
# 否则celery的task调用socketio不成功
socketio = SocketIO(app, message_queue='amqp://guest:guest@localhost:5672//')
namespace = '/task'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task')
def start_background_task():
    from celery_app import background_task
    background_task.delay()
    return 'Started'


if __name__ == '__main__':
    socketio.run(app)
