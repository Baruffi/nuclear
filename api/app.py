from redis import Redis
from flask import Flask, abort
import logging.config
from provider.sensor_provider import sensors, get_sensor

logging.config.fileConfig(fname='log.conf')

redis = Redis(host='redis', port=6379)
app = Flask(__name__)


@app.route('/<id>', defaults={'external': 0.0})
@app.route('/<id>/<float:external>', methods=['GET'])
def read(id: str, external: float):
    sensor = get_sensor(id)
    if sensor:
        return sensor.read(external)
    else:
        abort(404)


@app.route('/startup', methods=['POST'])
def startup():
    all_startups = {sensor.get_id(): 'startup' for sensor in sensors}
    redis.hmset('stage', all_startups)
    return ('', 204)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    all_shutdowns = {sensor.get_id(): 'shutdown' for sensor in sensors}
    redis.hmset('stage', all_shutdowns)
    return ('', 204)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
