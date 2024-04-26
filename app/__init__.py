from flask import Flask
import redis
import os
from rq import Queue

app = Flask(__name__)

# Set up redis connection
redis_url = os.getenv("REDIS_URL", "redis://127.0.0.1:6379")
conn = redis.from_url(redis_url, password=os.getenv("REDIS_PASSWORD", ""))

# Connect to redis queue
redQueue = Queue(connection=conn)

from app import routes