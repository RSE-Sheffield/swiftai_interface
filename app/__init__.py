from flask import Flask
from flask_session import Session
import redis
import os
import rq_dashboard
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

# Set up rq-dashboard
app.config["RQ_DASHBOARD_REDIS_URL"] = redis_url
rq_dashboard.web.setup_rq_connection(app)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/queue")

from app import routes