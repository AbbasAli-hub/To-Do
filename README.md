# To-Do App

A containerized to-do application built in Python, with an automated CI/CD pipeline and deployment to AWS EC2.

## Features

- Create, update, and delete tasks
- Data persistence using Docker volumes
- Containerized with Docker and Docker Compose
- Automated CI pipeline (GitHub Actions) that runs on every push
- Automated Docker image build on every push to `main`
- Deployed on an AWS EC2 instance

## Tech Stack

- **Language:** Python
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS EC2
- **Version Control:** Git, GitHub

## Architecture

```
User → EC2 Instance → Docker Container (App) → Docker Volume (Persistent Data)
```

Every push to `main` triggers two GitHub Actions workflows:
1. **Python CI** — runs tests/checks against the codebase
2. **Docker Build** — builds and pushes the Docker image

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Run Locally
```bash
git clone https://github.com/AbbasAli-hub/To-Do.git
cd To-Do
docker-compose up --build
```

The app will be available at `http://localhost:<PORT>`.

### Stop the App
```bash
docker-compose down
```

## CI/CD Pipeline

This project uses GitHub Actions for automation:
- `python-ci.yml` — validates the Python code on every push
- `docker-build.yml` — builds the Docker image on every push to `main`

View the live workflow runs [here](https://github.com/AbbasAli-hub/To-Do/actions).

## Deployment

The application is deployed on an AWS EC2 instance using Docker Compose, with persistent data managed through Docker volumes.

## What This Project Demonstrates

- Containerizing an application with Docker and Docker Compose
- Building a CI/CD pipeline with GitHub Actions
- Managing persistent storage in containers
- Deploying and running an application on AWS EC2

## Author

**Mohammed Abbas Ali**
[LinkedIn](https://linkedin.com/in/abbasali01) · [GitHub](https://github.com/AbbasAli-hub)
