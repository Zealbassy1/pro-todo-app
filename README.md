The application allows users to register for an account, log in, and manage their own personal to-do lists with full CRUD (Create, Read, Update, Delete) functionality.

🚀 Tech Stack & Tools
This project utilizes a modern and robust set of technologies to cover all aspects of the development and deployment lifecycle.

Backend: Python with the Flask web framework.

Frontend: HTML templates with Tailwind CSS for styling.

Database: MySQL.

Containerization: Docker & Docker Compose.

Cloud Provider: Amazon Web Services (AWS).

CI/CD: GitHub Actions.

Key AWS Services Used:
Amazon RDS (Relational Database Service): For a managed, production-grade MySQL database.

Amazon EC2 (Elastic Compute Cloud): To host our application on a virtual server.

IAM (Identity and Access Management): For secure management of AWS credentials.

⚙️ The DevOps Workflow
This project was built by following a structured, multi-phase DevOps lifecycle:

Phase 1: Local Development
The full-stack Flask application was built and tested on a local machine. This included setting up a Python virtual environment, creating the database schema with SQLAlchemy, and developing the user authentication and to-do list features.

Phase 2: Containerization
The application was containerized using Docker to ensure consistency across different environments. A Dockerfile was created to define the application image. Docker Compose was then used to orchestrate a multi-container local environment, linking the Flask application container with a separate MySQL database container and solving networking challenges.

Phase 3: Cloud Infrastructure Provisioning
The necessary infrastructure to host the application in a production-like environment was provisioned on AWS. This involved:

Setting up a secure IAM user for programmatic access.

Launching a managed MySQL database using Amazon RDS.

Launching an Amazon EC2 virtual server and preparing it by installing Docker.

Phase 4: CI/CD Automation
A complete Continuous Integration and Continuous Deployment (CI/CD) pipeline was built using GitHub Actions. This pipeline automates the entire deployment process:

Trigger: The workflow runs automatically on every git push to the main branch.

Build: It builds a new Docker image of the Flask application.

Push: The newly built image is pushed to a Docker Hub repository.

Deploy: The workflow securely connects to the EC2 server via SSH, pulls the latest Docker image from Docker Hub, and runs it as a new container, making the updated application live.

Local Development with Docker
To run this application on your local machine using the containerized setup, ensure you have Docker and Docker Compose installed, then run:

docker-compose up --build

The application will be available at http://localhost:5000.