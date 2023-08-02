# Simple API for Social network app
---
This repository contains Webtroncs test task.
It implements an api for interacting with a social network.
You need to register and log in to access all features.

Brief description of existing endpoints:

- ```POST /auth/register``` to register new user
- ```POST /auth/jwt/login``` to login
- ```POST /auth/logout``` to logout

- ```POST /post/``` to create new post
- ```GET /post/``` to get list of all posts
- ```POST /post/{post_id}``` to update post
- ```GET /post/{post_id}``` to get desired post
- ```DELETE /post/{post_id}``` to delete post

- ```POST /post/{post_id}/reaction``` to set reaction
- ```GET /post/{post_id}/reaction``` to get list of all post reactions
- ```DELETE /post/{post_id}/reaction``` to delete your reaction

Full API documentation is available after the project is launched at
[Swagger](http://127.0.0.1:8000/docs) / [ReDoc](http://127.0.0.1:8000/redoc)

### Requirements
1. docker, docker compose
2. make

#### Run project locally
1. Clone the project to local machine 
```bash 
git clone https://github.com/zavr1k/webtronics-test.git
```
2. Run it with one command 
```bash
make compose
```
After that, the project will be available at http://127.0.0.1:8000/

3. To stop the project execute the command
```bash
make compose-down
```

#### Run manually
If you do not have ```make```  you can run the project manually.
1. Also clone the project
2. Create ```.env``` file with variables described in the ```.example.env``` or just copy that.
3. To run project execute command
```bash
docker-compose -f docker-compose.yaml up -d
```
4. To stop project execute command
```bash
docker-compose down
```
