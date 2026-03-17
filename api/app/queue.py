import redis

from app.config import settings


QUEUE_NAME = "job_queue"


def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_job(job_id: str) -> None:
    client = get_redis_client()
    client.rpush(QUEUE_NAME, job_id)