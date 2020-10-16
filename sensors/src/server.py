from flask import Flask
from redis import Redis
from sensor import Sensor, TemperatureSensor

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.route('/temperature')
def temperature():
    sensor = TemperatureSensor()
    return str(sensor.sense(1))


if __name__ == "__main__":
    app.run(host='0.0.0.0')