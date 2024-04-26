from flask import Flask
from flask_session import Session
import redis
import os
from rq import Queue

app = Flask(__name__)

# Set up redis connection
redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
conn = redis.from_url(redis_url, password=os.getenv("REDIS_PASSWORD", ""))

# Connect to redis queue
redQueue = Queue(connection=conn)

# Set up storing session variables in redis
# Uses as csv files are typically larger than usual for client side session data
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False # Current session will be lost on exit
app.config['SESSION_REDIS'] = conn

server_session = Session(app)

from app import routes