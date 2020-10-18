from flask import Flask
from redis import Redis
from model.sensors import TemperatureSensor

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

sensor = TemperatureSensor('CALDEIRA_1', 1000, 10)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.route('/temperature', defaults={'external': 0.0})
@app.route('/temperature/<float:external>')
def temperature(external):
    return sensor.read(external)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
