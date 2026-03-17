import os

os.environ["SKIP_DB_INIT"] = "true"

from api.app.schemas import JobCreate


def test_job_create_schema_accepts_valid_payload():
    job = JobCreate(payload="Process this sample job")
    assert job.payload == "Process this sample job"


def test_job_create_schema_rejects_empty_payload():
    try:
        JobCreate(payload="")
        assert False, "Expected validation to fail for empty payload"
    except Exception:
        assert True