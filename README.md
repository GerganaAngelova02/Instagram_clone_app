#Instagram clone app
A simple Instagram clone built using the Flask framework. This app allows users to create an account, upload pictures, and like and comment on pictures uploaded by other users.


Dockerfiles and set-up instructions for container-based development in different languages.

A simple Python Flask web server, aimed to be a starting point for further development. Comes with a Dockerfile image definition and Docker Compose script for easy dev environment setup.

Description
This is a Docker-based environment containing a simple Python Flask application. It is aimed at easy and quick onboarding to development within a Docker container. This allows for unified dependency management across different team members, and overall quick set up when starting a new project.

The idea is that the Docker image can be used in development and afterwards deployment on AWS or similar cloud provider. The Docker Compose file spawns a hot-reloading environment, where the ports used by each container are being exposed on the host machine.

The web server runs at port 8080. It overrides the default Flask port 5000, because Apple is now using it in the latest macOS version.

Getting Started
Before starting please get familiar with what Docker and Docker Compose are.

This is also a good overview of pros and cons when using Docker Compose for local development.

Dependencies
Docker
Port 8080 being available on host machine (your laptop)
Usage
After installing Docker, clone this repo and in the main folder run:

docker compose up -d
Note: If you are having troubles with docker compose try docker-compose instead.

This will spawn the running container in the background. When you then make changes to the code in the folder you will see the changes being reflected at localhost:8080.

To de-spawn the environment and remove the running containers execute:

docker compose down
Again, if there are issues with docker compose try docker-compose.
