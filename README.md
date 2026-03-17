# containerized-microservices

A multi-service containerized application built with FastAPI, Redis, PostgreSQL, and a background worker. This project demonstrates how multiple services communicate in a Docker Compose environment using asynchronous job processing.

## Overview

This repository is part of a DevOps/cloud portfolio and focuses on container orchestration, service-to-service communication, health checks, environment management, and persistent storage.

The system accepts jobs through an API, stores them in PostgreSQL, pushes them into a Redis queue, and processes them asynchronously through a worker service.

## Objectives

- Demonstrate multi-container application design
- Show service communication through Docker Compose networking
- Use Redis as a lightweight queue broker
- Use PostgreSQL as the system of record
- Implement health and readiness checks
- Show reproducible local development with Docker Compose and Makefile commands

## Architecture

```text
Client
  |
  v
FastAPI API
  |
  +--> PostgreSQL
  |
  +--> Redis queue
          |
          v
      Worker service
          |
          v
      PostgreSQL updates