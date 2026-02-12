# Operations Documentation

## Deployment

### Prerequisites
- Python 3.13+
- Poetry for dependency management
- PostgreSQL database (Neon recommended)

### Environment Setup
1. Clone the repository
2. Install dependencies: `poetry install`
3. Set up environment variables (see `.env.example`)

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `NEON_DATABASE_URL`: Neon PostgreSQL connection string (if using Neon)
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `DEBUG`: Enable/disable debug mode
- `ENVIRONMENT`: Environment name (dev, staging, prod)

### Running the Application
```bash
# Using Poetry
poetry run uvicorn src.main:app --reload

# Or using the factory pattern
poetry run uvicorn src.main:app --factory
```

## Database Migrations
The application uses Alembic for database migrations.

### Running Migrations
```bash
# Upgrade to latest version
poetry run alembic upgrade head

# Create a new migration
poetry run alembic revision --autogenerate -m "Description of changes"
```

## Docker Deployment
The application can be deployed using Docker.

### Building the Image
```bash
docker build -t fastapi-todo-backend .
```

### Running with Docker
```bash
docker run -d -p 8000:8000 --env-file .env fastapi-todo-backend
```

## Health Checks
The application provides a health check endpoint at `/health` that returns a 200 status code when the application is running properly.

## Logging
The application uses structured logging. Log levels can be controlled via the LOG_LEVEL environment variable.

## Monitoring
- Monitor the health endpoint for application status
- Track response times for performance
- Monitor error rates
- Watch database connection pools

## Security Considerations
- Rotate the JWT SECRET_KEY regularly
- Use HTTPS in production
- Implement proper firewall rules
- Regular security audits
- Monitor for suspicious activity

## Backup and Recovery
- Regular database backups
- Test backup restoration procedures
- Version control for application code
- Infrastructure as code for reproducible deployments

## Troubleshooting
### Common Issues
- Database connection errors: Check DATABASE_URL
- Authentication failures: Verify SECRET_KEY
- Performance issues: Check database indexes and connection pool settings

### Debugging
- Enable DEBUG mode for detailed error messages
- Check application logs
- Verify environment variables
- Test database connectivity