# Organization Management Service

A multi-tenant organization management system built with FastAPI and MongoDB.

## Project Structure

```
org-management-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   └── admin.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── organization_service.py
│   │   ├── admin_service.py
│   │   └── collection_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── organization_repository.py
│   │   └── admin_repository.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── organization_controller.py
│   │   └── admin_controller.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── database.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- MongoDB 4.4+

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd org-management-service
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` file with your configurations:
```
MONGODB_URL=mongodb://localhost:27017
MASTER_DB_NAME=master_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

5. Create all `__init__.py` files in each directory

6. Start MongoDB
```bash
mongod
```

7. Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Organization Endpoints

#### Create Organization
```http
POST /org/create
Content-Type: application/json

{
  "organization_name": "acme_corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

#### Get Organization
```http
GET /org/get?organization_name=acme_corp
```

#### Update Organization
```http
PUT /org/update?organization_name=acme_corp
Authorization: Bearer <token>
Content-Type: application/json

{
  "organization_name": "acme_corp_new",
  "email": "admin@acme.com",
  "password": "newsecurepassword123"
}
```

#### Delete Organization
```http
DELETE /org/delete?organization_name=acme_corp
Authorization: Bearer <token>
```

### Admin Endpoints

#### Admin Login
```http
POST /admin/login
Content-Type: application/json

{
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

## Architecture Design

### Multi-Tenant Architecture
- Master Database stores organization metadata and admin credentials
- Each organization gets its own MongoDB collection (e.g., `org_acme_corp`)
- Isolated data per organization

### Design Patterns
- Repository Pattern for data access abstraction
- Service Layer for business logic separation
- Dependency Injection for loose coupling
- JWT Authentication for stateless authentication

### Security
- Passwords hashed using bcrypt
- JWT tokens with expiration
- Authorization middleware for protected endpoints
- Organization-level access control

## Scalability Analysis

### Current Architecture Strengths
1. Collection-level isolation per organization
2. Horizontal scalability with MongoDB sharding
3. Stateless authentication with JWT
4. Modular design for easy extension

### Trade-offs and Limitations

#### Pros
- Simple implementation
- Fast query performance per organization
- Easy backup and restore per organization
- Clear data boundaries

#### Cons
- All collections in same database
- Limited to MongoDB's collection limits
- Cross-organization queries are complex
- Scaling requires database-level sharding

### Improved Architecture Suggestions

1. **Database-per-Tenant**: Each organization gets separate database for better isolation
2. **Microservices Architecture**: Separate services for auth, org management, tenant management
3. **Event-Driven Architecture**: Event sourcing for better audit trail
4. **Caching Layer**: Redis for organization metadata to reduce database load
5. **API Gateway Pattern**: Kong/Nginx for routing and rate limiting

### Technology Stack Alternatives

**Current**: FastAPI + MongoDB

**Alternative 1**: Django + PostgreSQL (better for complex relational data)
**Alternative 2**: NestJS + MongoDB (TypeScript type safety)
**Alternative 3**: Go + PostgreSQL (better performance and concurrency)