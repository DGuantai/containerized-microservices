# Architecture

## Purpose

This project demonstrates a multi-container microservices-style system running locally with Docker Compose.

## Components

### API service
Built with FastAPI. Responsible for:
- accepting job requests
- storing jobs in PostgreSQL
- enqueueing job IDs in Redis
- exposing health and readiness endpoints

### Worker service
A background Python process responsible for:
- blocking on the Redis queue
- retrieving queued job IDs
- updating job states in PostgreSQL
- simulating asynchronous job processing

### PostgreSQL
Stores persistent job data, including:
- job ID
- payload
- status
- timestamps

### Redis
Acts as the queue layer between the API and worker.

## Request Flow

1. Client sends a request to the API
2. API writes a new job row to PostgreSQL
3. API pushes the job ID into Redis
4. Worker retrieves the job ID from Redis
5. Worker updates the job status in PostgreSQL
6. Worker marks the job as completed after processing

## Networking

Docker Compose creates a private network for all services. Containers communicate using service names:

- `postgres`
- `redis`
- `api`
- `worker`

This is why the application does not use `localhost` for inter-service communication.

## Persistence

PostgreSQL uses a named volume so data remains available even if the container is recreated.