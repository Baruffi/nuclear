from redis import Redis
from logging import getLogger
from model.routines import Routine

logger = getLogger('app')
redis = Redis(host='redis', port=6379)

routines: list[Routine] = [
    Routine('power_modifier', {
            'startup': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            'running': [1],
            'shutdown': [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0],
            'stopped': [0],
            }),
    Routine('pressure_modifier', {
            'startup': [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2],
            'running': [1, 0.9, 0.8, 0.7, 0.8, 0.9],
            'shutdown': [1.2, 1, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
            'stopped': [0],
            }),
    Routine('flow_modifier', {
            'startup': [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2],
            'running': [1, 0.9, 0.8, 0.7, 0.8, 0.9],
            'shutdown': [1.2, 1, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
            'stopped': [0],
            }),
    Routine('temperature_modifier', {
            'startup': [0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.6, 0.9, 0.9, 1.2, 1.2],
            'running': [1, 1, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.8, 0.8, 0.9, 0.9],
            'shutdown': [1.2, 1.2, 0.9, 0.9, 0.6, 0.6, 0.4, 0.4, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05],
            'stopped': [0.05],
            })
]


def get_routine_stage(id: str, stage: str):
    return next((routine.get_stage(stage) for routine in routines if routine.get_id() == id))


def time_cycle(id: str):
    with redis.lock('update'):
        sensor = str(redis.get('sensor'), 'utf-8')
        stage = str(redis.get('stage'), 'utf-8')
        if not redis.hexists(id, sensor):
            redis.hset(id, sensor, 0)

    def decorator(func):
        def decorated(*args, **kwargs):
            routine_stage = get_routine_stage(id, stage)

            with redis.lock('update'):
                current_cycle = int(redis.hget(id, sensor))

                if current_cycle == len(routine_stage) - 1:
                    # if ended startup, auto-update to running
                    if stage == 'startup':
                        redis.set('stage', 'running')

                    # if ended shutdown, auto-update to stopped
                    if stage == 'shutdown':
                        redis.set('stage', 'stopped')

                    redis.hset(id, sensor, 0)
                else:
                    redis.hincrby(id, sensor, 1)

            value = routine_stage[current_cycle]

            logger.info('%s %s %s %d %f', id, sensor,
                        stage, current_cycle, value)

            return func(*args, **kwargs, **{id: value})

        return decorated

    return decorator
