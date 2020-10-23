from redis import Redis
from random import normalvariate
from logging import getLogger
from provider.routine_provider import get_routine

redis = Redis(host='redis', port=6379)

logger = getLogger('app')


class Sensor(object):

    def __init__(self, id: str, mean: float = 0, variance: float = 0):
        self.id = id
        self.mean = mean
        self.variance = variance

    def get_id(self):
        return self.id

    def get_updated_modifier(self, modifier):
        with redis.lock('update'):
            if not redis.hexists('stage', self.id):
                redis.hset('stage', self.id, 'startup')

            if not redis.hexists(modifier, self.id):
                redis.hset(modifier, self.id, 0)

            curent_stage = str(redis.hget('stage', self.id), 'utf-8')
            current_cycle = int(redis.hget(modifier, self.id))

            routine_stage = get_routine(modifier).get_stage(curent_stage)

            if current_cycle >= len(routine_stage) - 1:
                # if ended startup, auto-update to running
                if curent_stage == 'startup':
                    redis.hset('stage', self.id, 'running')

                # if ended shutdown, auto-update to stopped
                if curent_stage == 'shutdown':
                    redis.hset('stage', self.id, 'stopped')

                redis.hset(modifier, self.id, 0)
            else:
                redis.hincrby(modifier, self.id)

        current_modifier = routine_stage[current_cycle]

        logger.info('%s %s %s %d %f', modifier, self.id,
                    curent_stage, current_cycle, current_modifier)

        return current_modifier

    def read(self, external: float):
        return {
            'id': self.id,
            'external': str(external)
        }


class PowerSensor(Sensor):

    def read(self, external: float):
        raw_value = normalvariate(self.mean, self.variance)
        modifier = self.get_updated_modifier('power_modifier')

        value = round(raw_value * modifier + external, 5)

        return {
            'id': self.id,
            'external': str(external),
            'value': str(value),
            'unit': 'MW',
        }


class PressureSensor(Sensor):

    def read(self, external: float):
        raw_value = normalvariate(self.mean, self.variance)
        modifier = self.get_updated_modifier('pressure_modifier')

        value = round(raw_value * modifier + external, 5)

        return {
            'id': self.id,
            'external': str(external),
            'value': str(value),
            'unit': 'MPa',
        }


class FlowSensor(Sensor):

    def read(self, external: float):
        raw_value = normalvariate(self.mean, self.variance)
        modifier = self.get_updated_modifier('flow_modifier')

        value = round(raw_value * modifier + external, 5)

        return {
            'id': self.id,
            'external': str(external),
            'value': str(value),
            'unit': 't/h',
        }


class TemperatureSensor(Sensor):

    def read(self, external: float):
        raw_value = normalvariate(self.mean, self.variance)
        modifier = self.get_updated_modifier('temperature_modifier')

        value = round(raw_value * modifier + external, 5)

        return {
            'id': self.id,
            'external': str(external),
            'value': str(value),
            'unit': 'ºC',
        }
