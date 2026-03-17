import redis

from app.config import settings


QUEUE_NAME = "job_queue"


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def dequeue_job(timeout: int = 5) -> str | None:
    client = get_redis_client()
    item = client.blpop(QUEUE_NAME, timeout=timeout)
    if item is None:
        return None

    _, job_id = item
    return job_id