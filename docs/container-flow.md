# Container Flow

## Startup Sequence

The stack is started through Docker Compose.

### PostgreSQL
Starts first and becomes healthy when `pg_isready` succeeds.

### Redis
Starts and becomes healthy when `redis-cli ping` succeeds.

### API
Waits for PostgreSQL and Redis to be healthy before starting.

### Worker
Also waits for PostgreSQL and Redis to be healthy before starting.

## Why Health Checks Matter

Container startup order alone is not enough. A container can be running but not ready.

This project uses health checks to reduce startup race conditions and improve reliability.

## Job Processing Flow

1. API receives a new job
2. API stores the job in PostgreSQL with `queued` status
3. API pushes the job ID to Redis
4. Worker reads the job ID using `BLPOP`
5. Worker sets the job status to `processing`
6. Worker simulates work
7. Worker updates the job status to `completed`

## Logging Flow

Logs can be viewed with:

```bash
make logs