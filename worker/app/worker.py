import logging
import time
from datetime import datetime, timezone

from app.config import settings
from app.db import Job, SessionLocal
from app.queue import dequeue_job


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("worker")


def process_job(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)

        if not job:
            logger.warning("Job %s not found in database", job_id)
            return

        logger.info("Starting job %s", job_id)
        job.status = "processing"
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        time.sleep(settings.worker_poll_seconds)

        job.status = "completed"
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        logger.info("Completed job %s", job_id)

    except Exception as exc:
        logger.exception("Failed processing job %s: %s", job_id, exc)

        try:
            job = db.get(Job, job_id)
            if job:
                job.status = "failed"
                job.updated_at = datetime.now(timezone.utc)
                db.commit()
        except Exception:
            logger.exception("Failed to update job %s to failed state", job_id)

    finally:
        db.close()


def main() -> None:
    logger.info("Worker started and waiting for jobs")

    while True:
        try:
            job_id = dequeue_job(timeout=5)

            if job_id is None:
                continue

            process_job(job_id)

        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            break
        except Exception as exc:
            logger.exception("Worker loop error: %s", exc)
            time.sleep(2)


if __name__ == "__main__":
    main()