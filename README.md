# Instagram clone app :camera:
A simple Instagram clone built using the Flask framework. This app allows users to create an account, upload pictures, and like and comment on photos,follow and unfollow other users.

## Features :sparkles:
* User authentication and authorization.
* User account settings.
* Picture uploads.:framed_picture:
* Displaying uploaded images on the user's profile feed page.
* Explore page. :compass:
* Ability to like :heart: and comment :left_speech_bubble: on images, see likes count, and list users who have commented on a single post.
* User profile pages with the ability to follow and unfollow other users, and see the number of posts, followers, and following accounts.

## Prerequisites :scroll:
* Docker
* Docker Compose
* Postman 

## Description 
Docker is a containerization technology that allows developers to package their applications and dependencies into containers. These containers can then be run on any machine that has Docker installed, making it easy to develop and test applications on different environments.

In this project, we are using Docker to isolate our application and its dependencies from the host system. This ensures that the application runs consistently, regardless of the host system's configuration.

## Getting Started :sparkles:
Make sure [Docker](https://www.docker.com/products/docker-desktop/) is installed.
Get familiar with what [Docker](https://docs.docker.com/get-started/overview/) and [Docker Compose](https://docs.docker.com/compose/).\
After installing Docker, clone this repo and in the main folder execute the following commands:

## Docker Commands :round_pushpin:

### Start Docker
```
docker-compose up 
```

### Remove Docker Containers(does not remove database)
```
docker-compose down
```

###  Remove Docker Containers and the Databases
```
docker-compose down -v
```

## Database Setup

Run `db_setup.py` once to create all tables.\
View the records in database on [phpMyAdmin](http://localhost:8090/) \
**Note:** the link is available only if the docker container is running.

## Testing :heavy_check_mark:
* Running the tests. Each test makes an HTTP request to the server and the changes from the response can be seen in the database.
* Another way for testing is to send requests through Postman. 

