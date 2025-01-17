# fastapi_postgresql

This creates a REST API that support CRUD operations for discussion forum components such as users, topics, posts, and categories.

## Introduction

This project uses FastAPI and SQLModel to create the API and it's endpoints. PostgreSQL is used as the database backend.


## Setup

Clone the repository:
```
git clone https://github.com/RLee2004/fastapi_postgresql.git
```

Install necessary libraries:
```
pip install SQLModel, bcrypt, fastapi, uvicorn
```

Change database url in database.py

Run using uvicorn:
```
uvicorn main:app --reload
```
