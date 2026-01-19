#!/bin/bash
#
# Setup local PostgreSQL database for Image Hosting development
#
# Prerequisites:
#   - PostgreSQL installed and running locally
#   - psql command available
#   - Superuser access (typically 'postgres' user or your local user with createdb rights)
#
# Usage:
#   ./scripts/setup-local-db.sh
#
# This script creates:
#   - imagehosting_user (database user with password)
#   - imagehosting_dev (development database)

set -e

# Configuration
DB_USER="imagehosting_user"
DB_PASSWORD="imagehosting_dev_password"
DB_DEV="imagehosting_dev"

echo "Setting up local PostgreSQL for Image Hosting..."
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo "Error: psql command not found. Please install PostgreSQL."
    exit 1
fi

# Function to run psql as superuser
run_psql() {
    psql -h localhost -U postgres -c "$1" 2>/dev/null || psql -c "$1" 2>/dev/null
}

# Create user if it doesn't exist
echo "Creating database user: $DB_USER"
run_psql "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1 || \
    run_psql "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
echo "  User ready."

# Create development database if it doesn't exist
echo "Creating development database: $DB_DEV"
if ! psql -h localhost -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw $DB_DEV && \
   ! psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw $DB_DEV; then
    run_psql "CREATE DATABASE $DB_DEV OWNER $DB_USER;"
fi
run_psql "GRANT ALL PRIVILEGES ON DATABASE $DB_DEV TO $DB_USER;"
echo "  Database ready."

echo ""
echo "Setup complete!"
echo ""
echo "Add these to your backend/.env for local development:"
echo ""
echo "  POSTGRES_HOST=localhost"
echo "  POSTGRES_PORT=5432"
echo "  POSTGRES_USER=$DB_USER"
echo "  POSTGRES_PASSWORD=$DB_PASSWORD"
echo "  POSTGRES_DB=$DB_DEV"
echo ""
echo "Next steps:"
echo "  1. Update backend/.env with the values above"
echo "  2. Run migrations: cd backend && uv run alembic upgrade head"
echo "  3. Start server: uv run uvicorn app.main:app --reload"
