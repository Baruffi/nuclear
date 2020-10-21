from redis import Redis
from logging import getLogger

redis = Redis(host='redis', port=6379)

logger = getLogger('app')


def time_cycle(id: str, values: list[list[float, int]]):
    values = list(zip(*values[::-1]))

    with redis.lock('setup'):
        if not redis.exists(id + '_cycle'):
            redis.lpush(id + '_cycle', *values[0])

        if not redis.exists(id + '_delay'):
            redis.lpush(id + '_delay', *values[1])

        if not redis.exists(id + '_count'):
            redis.set(id + '_count', 0)

    def decorator(func):
        def decorated(*args, **kwargs):
            with redis.lock('update'):
                current_cycle = float(redis.lindex(id + '_cycle', 0))
                current_delay = int(redis.lindex(id + '_delay', 0))
                current_count = int(redis.get(id + '_count'))

                if current_count >= current_delay:
                    redis.set(id + '_count', 0)
                    redis.lpush(id + '_delay', redis.rpop(id + '_delay'))
                    redis.lpush(id + '_cycle', redis.rpop(id + '_cycle'))
                else:
                    redis.incr(id + '_count')

            logger.info('%s %f %f %f', id, current_cycle, current_delay,
                        current_count)

            return func(*args, **kwargs, **{id: float(current_cycle)})

        return decorated

    return decorator
