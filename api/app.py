from redis import Redis
from flask import Flask, abort
import logging.config
from logging import getLogger
from model.sensors import Sensor, PowerSensor, PressureSensor, FlowSensor, TemperatureSensor


logging.config.fileConfig(fname='log.conf')
logger = getLogger('app')

redis = Redis(host='redis', port=6379)
app = Flask(__name__)

sensors: list[Sensor] = [
    PowerSensor('GEP', 450, 8.722),
    PressureSensor('SG1FWP', 5.2, 0.03793),
    PressureSensor('SG2FWP', 5.2, 0.04199),
    FlowSensor('SG1FWF', 120, 25.34),
    FlowSensor('SG2FWF', 90, 33.63),
    PressureSensor('SG1SP', 6.4, 0.02893),
    PressureSensor('SG2SP', 6.4, 0.02927),
    FlowSensor('SG1SF', 140, 35.04),
    FlowSensor('SG2SF', 100, 44.91),
    TemperatureSensor('DTL1', 177, 0.6807),
    TemperatureSensor('DTL2', 93, 0.6615)
]

if not redis.exists('stage'):
    redis.set('stage', 'startup')


@app.route('/<id>', defaults={'external': 0.0})
@app.route('/<id>/<float:external>', methods=['GET'])
def read(id: str, external: float):
    return next((sensor.read(external) for sensor in sensors if sensor.get_id() == id), None) or abort(404)


@app.route('/startup', methods=['POST'])
def startup():
    if 'running' != str(redis.get('stage'), 'utf-8') != 'startup':
        redis.set('stage', 'startup')


@app.route('/shutdown', methods=['POST'])
def shutdown():
    if 'stopped' != str(redis.get('stage'), 'utf-8') != 'shutdown':
        redis.set('stage', 'shutdown')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
