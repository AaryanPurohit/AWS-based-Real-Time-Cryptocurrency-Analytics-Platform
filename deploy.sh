#!/bin/bash

# AWS Crypto Analytics Platform - Deployment Script
# This script deploys the entire platform to AWS
# Demonstrates Infrastructure as Code and CI/CD practices

set -e

echo "🚀 Starting AWS Crypto Analytics Platform Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="aws-crypto-analytics"
ENVIRONMENT=${1:-dev}
AWS_REGION=${2:-us-east-1}

echo -e "${BLUE}Deploying to environment: ${ENVIRONMENT}${NC}"
echo -e "${BLUE}AWS Region: ${AWS_REGION}${NC}"

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        echo -e "${RED}Terraform is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}Node.js is not installed. Please install it first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All prerequisites are satisfied!${NC}"
}

# Deploy infrastructure
deploy_infrastructure() {
    echo -e "${YELLOW}Deploying AWS infrastructure with Terraform...${NC}"
    
    cd infrastructure
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="environment=${ENVIRONMENT}" -var="aws_region=${AWS_REGION}"
    
    # Apply infrastructure
    terraform apply -var="environment=${ENVIRONMENT}" -var="aws_region=${AWS_REGION}" -auto-approve
    
    # Get outputs
    KINESIS_STREAM=$(terraform output -raw kinesis_stream_name)
    DYNAMODB_TABLE=$(terraform output -raw dynamodb_table_name)
    REDIS_ENDPOINT=$(terraform output -raw redis_endpoint)
    S3_BUCKET=$(terraform output -raw s3_bucket_name)
    
    echo -e "${GREEN}Infrastructure deployed successfully!${NC}"
    echo -e "${BLUE}Kinesis Stream: ${KINESIS_STREAM}${NC}"
    echo -e "${BLUE}DynamoDB Table: ${DYNAMODB_TABLE}${NC}"
    echo -e "${BLUE}Redis Endpoint: ${REDIS_ENDPOINT}${NC}"
    echo -e "${BLUE}S3 Bucket: ${S3_BUCKET}${NC}"
    
    cd ..
}

# Deploy ML model
deploy_ml_model() {
    echo -e "${YELLOW}Deploying ML model to SageMaker...${NC}"
    
    cd ml-model
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Deploy model
    python deploy_model.py --environment ${ENVIRONMENT} --region ${AWS_REGION}
    
    echo -e "${GREEN}ML model deployed successfully!${NC}"
    
    cd ..
}

# Deploy backend
deploy_backend() {
    echo -e "${YELLOW}Deploying FastAPI backend...${NC}"
    
    cd backend
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Create Lambda deployment package
    echo "Creating Lambda deployment package..."
    zip -r lambda_function.zip . -x "*.pyc" "__pycache__/*" "tests/*"
    
    echo -e "${GREEN}Backend deployment package created!${NC}"
    
    cd ..
}

# Deploy frontend
deploy_frontend() {
    echo -e "${YELLOW}Building and deploying React frontend...${NC}"
    
    cd frontend
    
    # Install dependencies
    npm install
    
    # Build for production
    npm run build
    
    # Deploy to S3 (if configured)
    if [ -n "$S3_BUCKET" ]; then
        echo "Deploying frontend to S3..."
        aws s3 sync build/ s3://${S3_BUCKET}/frontend/ --delete
        aws s3 website s3://${S3_BUCKET}/frontend/ --index-document index.html --error-document index.html
    fi
    
    echo -e "${GREEN}Frontend deployed successfully!${NC}"
    
    cd ..
}

# Start data pipeline
start_data_pipeline() {
    echo -e "${YELLOW}Starting data pipeline...${NC}"
    
    cd data-pipeline
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Set environment variables
    export KINESIS_STREAM_NAME=${KINESIS_STREAM}
    export AWS_REGION=${AWS_REGION}
    export FETCH_INTERVAL=60
    
    # Start producer in background
    echo "Starting Kinesis producer..."
    nohup python kinesis_producer.py > producer.log 2>&1 &
    
    echo -e "${GREEN}Data pipeline started!${NC}"
    echo -e "${BLUE}Producer PID: $!${NC}"
    echo -e "${BLUE}Logs: data-pipeline/producer.log${NC}"
    
    cd ..
}

# Start backend server
start_backend() {
    echo -e "${YELLOW}Starting FastAPI backend server...${NC}"
    
    cd backend
    
    # Set environment variables
    export DYNAMODB_TABLE=${DYNAMODB_TABLE}
    export REDIS_ENDPOINT=${REDIS_ENDPOINT}
    export S3_BUCKET=${S3_BUCKET}
    
    # Start server
    echo "Starting FastAPI server on port 8000..."
    nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
    
    echo -e "${GREEN}Backend server started!${NC}"
    echo -e "${BLUE}Server PID: $!${NC}"
    echo -e "${BLUE}API URL: http://localhost:8000${NC}"
    echo -e "${BLUE}Logs: backend/backend.log${NC}"
    
    cd ..
}

# Start frontend
start_frontend() {
    echo -e "${YELLOW}Starting React frontend...${NC}"
    
    cd frontend
    
    # Start development server
    echo "Starting React development server on port 3000..."
    nohup npm start > frontend.log 2>&1 &
    
    echo -e "${GREEN}Frontend started!${NC}"
    echo -e "${BLUE}Frontend PID: $!${NC}"
    echo -e "${BLUE}Frontend URL: http://localhost:3000${NC}"
    echo -e "${BLUE}Logs: frontend/frontend.log${NC}"
    
    cd ..
}

# Health check
health_check() {
    echo -e "${YELLOW}Performing health checks...${NC}"
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
    else
        echo -e "${RED}✗ Backend health check failed${NC}"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend is healthy${NC}"
    else
        echo -e "${RED}✗ Frontend health check failed${NC}"
    fi
    
    echo -e "${GREEN}Health checks completed!${NC}"
}

# Main deployment function
main() {
    echo -e "${BLUE}=== AWS Crypto Analytics Platform Deployment ===${NC}"
    
    check_prerequisites
    deploy_infrastructure
    deploy_ml_model
    deploy_backend
    deploy_frontend
    start_data_pipeline
    start_backend
    start_frontend
    
    # Wait a moment for services to start
    sleep 10
    
    health_check
    
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo -e "${BLUE}Frontend: http://localhost:3000${NC}"
    echo -e "${BLUE}Backend API: http://localhost:8000${NC}"
    echo -e "${BLUE}API Documentation: http://localhost:8000/docs${NC}"
    echo -e "${YELLOW}To stop all services, run: ./stop.sh${NC}"
}

# Run main function
main "$@" 