#!/bin/bash

# AWS Crypto Analytics Platform - Stop Script
# Stops all services and cleans up resources

set -e

echo "🛑 Stopping AWS Crypto Analytics Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Stop background processes
stop_processes() {
    echo -e "${YELLOW}Stopping background processes...${NC}"
    
    # Find and kill Python processes
    pkill -f "kinesis_producer.py" || true
    pkill -f "uvicorn app:app" || true
    pkill -f "npm start" || true
    
    echo -e "${GREEN}Background processes stopped!${NC}"
}

# Clean up local files
cleanup_local() {
    echo -e "${YELLOW}Cleaning up local files...${NC}"
    
    # Remove log files
    rm -f data-pipeline/producer.log
    rm -f backend/backend.log
    rm -f frontend/frontend.log
    
    # Remove build artifacts
    rm -rf frontend/build
    rm -rf backend/__pycache__
    rm -rf data-pipeline/__pycache__
    
    # Remove model artifacts
    rm -rf ml-model/model_*
    
    echo -e "${GREEN}Local cleanup completed!${NC}"
}

# Destroy infrastructure (optional)
destroy_infrastructure() {
    echo -e "${YELLOW}Do you want to destroy AWS infrastructure? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${YELLOW}Destroying AWS infrastructure...${NC}"
        
        cd infrastructure
        
        # Destroy with Terraform
        terraform destroy -auto-approve
        
        cd ..
        
        echo -e "${GREEN}Infrastructure destroyed!${NC}"
    else
        echo -e "${BLUE}Infrastructure cleanup skipped.${NC}"
    fi
}

# Main stop function
main() {
    echo -e "${BLUE}=== Stopping AWS Crypto Analytics Platform ===${NC}"
    
    stop_processes
    cleanup_local
    
    echo -e "${YELLOW}Do you want to destroy AWS infrastructure? This will remove all AWS resources.${NC}"
    destroy_infrastructure
    
    echo -e "${GREEN}🎉 Platform stopped successfully!${NC}"
    echo -e "${BLUE}To restart, run: ./deploy.sh${NC}"
}

# Run main function
main "$@" 