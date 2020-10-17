from flask import Flask
from redis import Redis
from model.sensors import TemperatureSensor

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


@app.route('/temperature')
def temperature():
    sensor = TemperatureSensor(10)
    return sensor.read(1)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
