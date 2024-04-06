# CMS-SERVER-API-GATEWAY

CMS-SERVER-USERS is a microservice in a system built using microservices architecture. It handles user-related operations as comments and user profile management.

## How it works

The user service is built using Flask The user service is configured to run in different environments (development, testing, production) with different settings for each environment. The configuration is done through a Config class and its subclasses, and can be easily adjusted via environment variables.

To interact with the server, you can use the following API endpoints:

- **GET /users/{id}**: Get user details by ID.
- **GET /users/{username}**: Get user details by username.
- **GET /users**: Get a list of all users.
- **POST /users/register**: Register a new user.
- **POST /users/activate**: Activate a user.
- **PUT /users/{id}**: Update user details by ID.
- **DELETE /users/{id}**: Delete a user by ID.
- **POST /users/credentials**: Verify given credentials.

- **GET users/comments/{id}**: Get comment details by ID.
- **GET users/comments**: Get a list of all comments.
- **POST users/comments**: Add a new comment.
- **DELETE users/comments/{id}**: Delete a comment by ID.
- **GET users/comments/user/{id}**: Get comments by user ID.
- **GET users/comments/article/{id}**: Get comments by article ID.

## Quickstart

1. Set the environment variables

```bash
export SECRET_KEY=<your-secret-key>
export DATABASE_URL=<your-database-url>
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

4. Make database migrations

```bash
docker exec -it <users-container-id> bash
pipenv run flask --app users.app.py db upgrade head
```

## Deployment

For deployment, make sure that DEBUG is set to 0, so ProductionConfig is used. Additionally, you should set the database URL.

## Tests

To run all app tests, use the following command

```bash
pipenv run pytest
```
