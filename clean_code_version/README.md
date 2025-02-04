# Pasal-ko-Website Clean Architecture Version

This is a refactored version of Pasal-ko-Website using Clean Architecture principles and Vertical Slice Architecture.

## Project Structure

```
src/
├── auth/                      # Authentication Vertical Slice
│   ├── domain/               # Domain layer
│   │   ├── entities/        # Domain entities
│   │   ├── repositories/    # Repository interfaces
│   │   └── services/        # Domain services
│   ├── infrastructure/       # Infrastructure layer
│   │   ├── models.py        # Database models
│   │   └── repositories/    # Repository implementations
│   ├── application/         # Application layer
│   │   └── use_cases/      # Use cases/application services
│   └── presentation/        # Presentation layer
│       └── router.py        # API routes
├── posts/                    # Posts Vertical Slice
├── votes/                    # Votes Vertical Slice
└── shared/                   # Shared components
    ├── infrastructure/      # Shared infrastructure
    └── config.py           # Configuration
```

## Architecture Overview

This project follows Clean Architecture principles with Vertical Slice Architecture:

1. **Domain Layer**: Contains business logic, entities, and interfaces
2. **Infrastructure Layer**: Implements interfaces defined in the domain layer
3. **Application Layer**: Contains use cases and orchestrates the domain layer
4. **Presentation Layer**: Handles HTTP requests and responses

Each vertical slice (auth, posts, votes) is a self-contained feature with its own layers.

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
