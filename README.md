# Training Management System

## Table of Contents
- [Overview](#overview)
- [Microservices](#microservices)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Setup Instructions](#setup-instructions)
  - [Clone the Repository](#clone-the-repository)
  - [Build and Run Services](#build-and-run-services)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
  - [Setting Up EC2 Instance](#setting-up-ec2-instance)
  - [Manual Deployment](#manual-deployment)

## Overview
The Training Management System is a microservices-based application designed to manage various aspects of training programs, including students, trainers, courses, and bookings. The system is composed of multiple services, each responsible for a specific domain, allowing for scalability and maintainability.

## Microservices
The application consists of the following microservices:

- **API Gateway**: Serves as the entry point for all client requests and routes them to the appropriate service.
- **Student Service**: Manages student registrations, retrievals, and related operations.
- **Trainer Service**: Handles trainer registrations and information retrieval.
- **Course Service**: Manages course details and offerings.
- **Booking Service**: Manages the booking of courses for students.
- **Authentication Service**: Handles user authentication and authorization.
- **Frontend**: Provides a user interface for interacting with the training management system.

## Technologies Used
- **Python**: Backend services are built using Python.
- **Flask**: Each microservice is developed using the Flask framework.
- **DynamoDB**: NoSQL database for storing service data.
- **Docker**: Containerization of services for easy deployment and scaling.
- **GitHub Actions**: Continuous Integration and Continuous Deployment (CI/CD) setup.

## Prerequisites
- Docker and Docker Compose installed on your machine.
- AWS credentials for DynamoDB setup.
- Python 3.8 or higher (for local testing).
- Git for version control.

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/ivflit/TrainingCompanyFlask.git
cd TrainingCompanyFlask
```

### Environment variables

Create a .env file in the root directory and add the variables shown in .env example making sure to replace the secret keys

### Build and Run Services

```bash
docker-compose up --build
```

Services will be accessible at the following ports:

- API Gateway: http://localhost:8000
- Student Service: http://localhost:8002
- Booking Service: http://localhost:8003
- Course Service: http://localhost:8004
- Trainer Service: http://localhost:8005
- Authentication Service: http://localhost:8006
- Frontend: http://localhost:8007

## Running Tests

Firstly, create a virtual environment within the test directory and install the requirements 

```bash
# Navigate to tests directory
cd tests

# For Unix/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# For Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

cd ../
```

To run the tests you need to be in the root of the project and ensure you are in the tests virtual environment

To run a singular test, Enter:

```bash
python -m pytest tests/test_service.py
```

To run all of them at once, run

```bash
pytest tests/test_service.py
```

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD. Upon pushing to the master branch:

Tests are automatically run.
If all tests pass, the code is deployed to an EC2 instance.

### Deployment

### Setting Up EC2 Instance
To set up the EC2 instance for running the application:

Launch an EC2 Instance:

Choose an Amazon Machine Image (AMI) (e.g., Ubuntu).
Select an instance type (e.g., t2.micro).
Configure security groups to allow SSH (port 22) and HTTP (port 80) access.

SSH into the EC2 Instance:
```bash
ssh -i <your_key.pem> ubuntu@<your_ec2_public_ip>

```
Install Docker and Docker Compose:

```bash
# Update package information
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start Docker and enable it to run on boot
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo apt-get install -y python3-pip
sudo pip3 install docker-compose
```

Clone the Project Repository:

```bash
git clone https://github.com/ivflit/TrainingCompanyFlask.git
cd TrainingCompanyFlask
```

### Manual Deployment

SSH into your EC2 instance and navigate to the project directory:

```bash
ssh -i <your_key.pem> ubuntu@<your_ec2_public_ip>
cd path/to/your/cloned/project
```

Run this to deploy:

```bash
# Pull the latest code from GitHub
git pull origin master

# Build and run the Docker containers
docker-compose up --build -d
```

If you want to check if any Docker containers are currently running, you can use the following command:

```bash
docker ps
```

If there are any running then run the following to stop all running containers that were started by Docker Compose:

```bash
docker-compose down
```