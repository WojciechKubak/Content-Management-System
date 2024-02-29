# CMS-SERVER-API-GATEWAY

CMS-SERVER-API-GATEWAY is a central point of entry into a system built using microservices architecture. It acts as a reverse proxy, routing requests from clients to services. It also handles non-business logic tasks like JWT authentication, authorization, and caching.

## How it works

The gateway service is built using Flask. It uses the Flask-JWT-Extended extension for handling JWTs and Flask-Caching for caching responses.

When a request is made to the gateway, it first passes through the JWT manager which checks for a valid JWT and handles any authentication errors. If the request is for a route that requires authentication and the JWT is valid, the request is then routed to the appropriate service (user or article). The response from the service is then cached and returned to the client.

The gateway service is configured to run in different environments (development, testing, production) with different settings for each environment. The configuration is done through a Config class and its subclasses, and can be easily adjusted via environment variables.

## Quickstart

1. Set the environment variables

```bash
export SECRET_KEY=<your-secret-key>
export USERS_URL=<your-users-service-url>
export ARTICLES_URL=<your-articles-service-url>
export DEBUG=1
```
2. Run the following commands to set up your environment

```bash
pip install pipenv
pipenv install --ignore-pipfile 
```

3. Run all containers
```bash
docker-compose up -d --build
```

## Deployment
For deployment, make sure that DEBUG is set to 0, so ProductionConfig is used. Additionally, you should set the Redis URL.

## Tests
To run all app tests, use the following command:
```bash
pipenv run pytest
```
