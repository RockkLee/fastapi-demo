# FastAPI Demo Project
This project is a demo application built using FastAPI, Docker, and SQLAlchemy.
It showcases a simple implementation of user and product APIs.
(Almost every function is written with async/await because FastAPI is an async framework.)

## Setup
1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd fastapi-demo
    ```
2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```
3. Build Dockerfile:
    ```sh
    docker build -t fastapi-demo .
    ```
4. Run the application using Docker Compose:
    ```sh
    docker-compose up -d
    ```
5. Access the API documentation:
    Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to see the Swagger UI.

## Using Pydantic
- Pydantic is used in this project to define data models for request and response bodies and validation.
- Schemas vs Model
  - Schemas means the classes for Pydantic, which are use for req&resp bodies and validation.
  - Model means the classes for SQLAlchemy, which are use for the orm objects.

### Example: User Schema
In `fastapi_demo/api/schemas/user.py`:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResp(BaseModel):
    id: int
    username: str
    email: str
```

## An Example of Creating an API Endpoint
### Define a router
- `fastapi_demo/api/routers/user_api.py`:
```python
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_demo.api.schemas.user import UserCreate, UserResp
from fastapi_demo.orm.connection import get_session
from fastapi_demo.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=['user_api']
)

@router.post("/create/", response_model=UserResp, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    user_service = UserService(db)
    created_user = await user_service.create_user(user)
    return created_user
```

### Register a router
- `main.py`:
```python
from fastapi import FastAPI
from fastapi_demo.api.routers import user_api

app = FastAPI()

app.include_router(user_api.router)
```

## Deploy this app with Gunicorn, Uvicorn workers, and Docker for parallel multi-processing
- Export dependencies from poetry.toml and exclude dev dependencies
    - `poetry export -f requirements.txt --output requirements.txt --without-hashes --only main`
- run Dockerfile
- run docker-compose.yml