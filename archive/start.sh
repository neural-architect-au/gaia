#!/bin/bash

# ClimateSolutionsAI Agent - Startup Script

echo "Starting ClimateSolutionsAI Agent..."
echo "Autonomous AI Agent for Climate Solutions"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: No .env file found. Creating from template..."
    cp .env.example .env
    echo "Please edit .env file with your AWS credentials before running again."
    echo "Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
    exit 1
fi

# Build and start services
echo "Building Docker images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check service health
echo "Checking service health..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "SUCCESS: Backend service is healthy"
else
    echo "ERROR: Backend service is not responding"
    echo "Backend logs:"
    docker-compose logs backend
fi

# Check frontend
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "SUCCESS: Frontend service is healthy"
else
    echo "ERROR: Frontend service is not responding"
    echo "Frontend logs:"
    docker-compose logs frontend
fi

echo ""
echo "ClimateSolutionsAI Agent is ready!"
echo ""
echo "Dashboard: http://localhost:8501"
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "To run the demo:"
echo "   python demo.py"
echo ""
echo "To stop services:"
echo "   docker-compose down"
echo ""
echo "Fighting climate change through autonomous AI!"
