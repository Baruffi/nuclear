from collections import deque
from redis import Redis


redis = Redis(host='redis', port=6379)


def time_cycle(id: str, values: list[list[float, int]]):
    redis.set(id + '_delay', 0)

    values = deque(values)

    def decorator(func):
        if int(redis.get(id + '_delay')) >= values[0][1]:
            redis.set(id + '_delay', 0)

            values.appendleft(values.pop())

        redis.incr(id + '_delay')

        def decorated(*args, **kwargs):
            return func(*args, **kwargs, **{id: values[0][0]})

        return decorated

    return decorator
