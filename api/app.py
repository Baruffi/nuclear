from redis import Redis
from flask import Flask, abort
import logging.config
from provider.sensor_provider import get_sensor

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
    with redis.lock('update'):
        raw_stages = redis.hgetall('stage')

        for key, value in raw_stages.items():
            str_key = str(key, 'utf-8')
            str_value = str(value, 'utf-8')

            if str_value in ['shutdown', 'stopped']:
                redis.hset('stage', str_key, 'startup')
                redis.hset('reset', str_key, 1)

    return ('Success', 200)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    with redis.lock('update'):
        raw_stages = redis.hgetall('stage')

        for key, value in raw_stages.items():
            str_key = str(key, 'utf-8')
            str_value = str(value, 'utf-8')

            if str_value in ['startup', 'running']:
                redis.hset('stage', str_key, 'shutdown')
                redis.hset('reset', str_key, 1)

    return ('Success', 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
