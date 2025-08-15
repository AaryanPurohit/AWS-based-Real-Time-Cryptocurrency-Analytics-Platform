# AWS Crypto Analytics Platform - Setup Guide

This guide will help you set up and deploy the complete AWS Crypto Analytics Platform, demonstrating your expertise with AWS services and microservices architecture.

## 🎯 Project Overview

This project showcases a real-time cryptocurrency analytics platform built entirely on AWS services, perfect for demonstrating your cloud and machine learning skills to potential employers.

### **AWS Services Used:**
- **Amazon Kinesis Data Streams** - Real-time data streaming
- **Amazon DynamoDB** - NoSQL database for real-time data
- **Amazon ElastiCache Redis** - In-memory caching
- **Amazon SageMaker** - Machine learning model hosting
- **Amazon Lambda** - Serverless functions
- **Amazon API Gateway** - REST API management
- **Amazon S3** - Data lake storage
- **Amazon CloudWatch** - Monitoring and logging
- **Amazon EC2** - Compute instances
- **Amazon VPC** - Networking infrastructure

## 📋 Prerequisites

Before starting, ensure you have the following installed:

### **Required Software:**
- **AWS CLI** - [Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **Terraform** - [Install Guide](https://developer.hashicorp.com/terraform/downloads)
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Docker** (optional) - [Download](https://www.docker.com/products/docker-desktop/)

### **AWS Account Setup:**
1. Create an AWS account if you don't have one
2. Create an IAM user with appropriate permissions
3. Configure AWS CLI with your credentials:
   ```bash
   aws configure
   ```

## 🚀 Quick Start

### **1. Clone and Setup Project**
```bash
# Navigate to your project directory
cd aws-crypto-analytics

# Make deployment scripts executable
chmod +x deploy.sh stop.sh
```

### **2. Configure AWS Credentials**
```bash
# Set up AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### **3. Deploy the Platform**
```bash
# Deploy everything with one command
./deploy.sh dev us-east-1
```

This will:
- Deploy AWS infrastructure using Terraform
- Deploy ML model to SageMaker
- Start data pipeline (Kinesis producer)
- Start backend API server
- Start frontend dashboard

### **4. Access the Application**
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
aws-crypto-analytics/
├── infrastructure/          # Terraform IaC
│   ├── main.tf             # Main infrastructure
│   └── modules/vpc/        # VPC module
├── backend/                 # FastAPI microservice
│   ├── app.py              # Main API
│   ├── lambda_function.py  # Lambda function
│   └── requirements.txt    # Python dependencies
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── App.js          # Main React app
│   │   └── components/     # React components
│   └── package.json        # Node.js dependencies
├── data-pipeline/          # Kinesis producer
│   ├── kinesis_producer.py # Data streaming
│   └── requirements.txt    # Python dependencies
├── ml-model/               # SageMaker ML model
│   ├── deploy_model.py     # Model deployment
│   └── requirements.txt    # ML dependencies
├── deploy.sh               # Deployment script
├── stop.sh                 # Cleanup script
└── README.md               # Project documentation
```

## 🔧 Manual Setup (Alternative)

If you prefer to set up components individually:

### **1. Deploy Infrastructure**
```bash
cd infrastructure
terraform init
terraform plan -var="environment=dev" -var="aws_region=us-east-1"
terraform apply -var="environment=dev" -var="aws_region=us-east-1" -auto-approve
cd ..
```

### **2. Deploy ML Model**
```bash
cd ml-model
pip install -r requirements.txt
python deploy_model.py --environment dev --region us-east-1
cd ..
```

### **3. Start Data Pipeline**
```bash
cd data-pipeline
pip install -r requirements.txt
export KINESIS_STREAM_NAME=crypto-price-stream-dev
export AWS_REGION=us-east-1
python kinesis_producer.py
```

### **4. Start Backend**
```bash
cd backend
pip install -r requirements.txt
export DYNAMODB_TABLE=crypto-prices-dev
export REDIS_ENDPOINT=your-redis-endpoint
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Start Frontend**
```bash
cd frontend
npm install
npm start
```

## 🎨 Features Demonstrated

### **Real-time Data Processing:**
- CoinGecko API integration
- Kinesis Data Streams for real-time streaming
- DynamoDB for real-time data storage
- ElastiCache Redis for caching

### **Machine Learning:**
- SageMaker model deployment
- Real-time price predictions
- ML model training and inference
- Auto-scaling ML endpoints

### **Microservices Architecture:**
- FastAPI backend service
- React frontend dashboard
- API Gateway integration
- Lambda serverless functions

### **AWS Best Practices:**
- Infrastructure as Code (Terraform)
- Security groups and IAM roles
- CloudWatch monitoring
- Auto-scaling and high availability

## 📊 Dashboard Features

The React dashboard includes:
- **Real-time price charts** with live updates
- **Market overview** with total market cap and volume
- **Individual cryptocurrency cards** with price changes
- **ML predictions** with confidence scores
- **AWS service status** indicators
- **Responsive design** for mobile and desktop

## 🔍 Monitoring and Logs

### **CloudWatch Dashboards:**
- Lambda function metrics
- Kinesis stream monitoring
- DynamoDB performance
- API Gateway metrics

### **Local Logs:**
- `data-pipeline/producer.log` - Kinesis producer logs
- `backend/backend.log` - FastAPI server logs
- `frontend/frontend.log` - React development logs

## 🛠️ Troubleshooting

### **Common Issues:**

1. **AWS Credentials Error:**
   ```bash
   aws configure
   # Enter your access key, secret key, and region
   ```

2. **Terraform State Issues:**
   ```bash
   cd infrastructure
   terraform init -reconfigure
   ```

3. **Port Conflicts:**
   ```bash
   # Check if ports are in use
   lsof -i :3000  # Frontend
   lsof -i :8000  # Backend
   ```

4. **Python Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### **Health Checks:**
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

## 🧹 Cleanup

To stop all services and clean up:

```bash
./stop.sh
```

This will:
- Stop all background processes
- Clean up local files
- Optionally destroy AWS infrastructure

## 📈 Scaling and Production

For production deployment:

1. **Use AWS ECS/EKS** for containerized deployment
2. **Set up CI/CD** with GitHub Actions or AWS CodePipeline
3. **Configure auto-scaling** for all services
4. **Set up monitoring** with CloudWatch and alarms
5. **Implement security** with AWS WAF and Shield
6. **Use CloudFront** for global content delivery

## 🎯 Job Interview Tips

This project demonstrates:

### **Technical Skills:**
- AWS service integration
- Microservices architecture
- Real-time data processing
- Machine learning deployment
- Infrastructure as Code
- API design and development

### **AWS Services Knowledge:**
- Kinesis Data Streams
- DynamoDB
- ElastiCache Redis
- SageMaker
- Lambda
- API Gateway
- S3
- CloudWatch
- VPC and networking

### **Best Practices:**
- Security and IAM
- Monitoring and logging
- Auto-scaling
- High availability
- Cost optimization

## 📚 Learning Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more AWS services
- Implementing additional ML models
- Improving the UI/UX
- Adding more data sources
- Implementing authentication
- Adding more analytics features

---

**Good luck with your AWS job interview! This project showcases comprehensive AWS expertise and modern cloud architecture skills.** 🚀 