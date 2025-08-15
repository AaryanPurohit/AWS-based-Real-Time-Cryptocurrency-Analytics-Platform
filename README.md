# 🚀 AWS Crypto Analytics Platform

A comprehensive real-time cryptocurrency analytics platform built entirely on AWS services, demonstrating advanced cloud architecture, microservices, and machine learning capabilities.

![AWS Services](https://img.shields.io/badge/AWS-Services-orange)
![Terraform](https://img.shields.io/badge/Terraform-IaC-blue)
![React](https://img.shields.io/badge/React-Frontend-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![SageMaker](https://img.shields.io/badge/SageMaker-ML-red)

## 🎯 Project Overview

This project showcases a production-ready cryptocurrency analytics platform that demonstrates expertise with multiple AWS services and modern cloud architecture patterns. Perfect for showcasing your AWS skills in job interviews!

### **🏗️ Architecture**

```
[CoinGecko API] → [Kinesis Producer (EC2)] → [Kinesis Data Streams]
                                                      ↓
[Lambda Functions] ← [API Gateway] ← [React Dashboard]
        ↓
[SageMaker ML Model] → [DynamoDB] → [ElastiCache Redis]
        ↓
[S3 Data Lake] → [CloudWatch Monitoring]
```

## 🚀 AWS Services Demonstrated

| Service | Purpose | Skills Demonstrated |
|---------|---------|-------------------|
| **Amazon Kinesis Data Streams** | Real-time data streaming | Event-driven architecture, streaming data processing |
| **Amazon DynamoDB** | NoSQL database | NoSQL design, real-time queries, auto-scaling |
| **Amazon ElastiCache Redis** | In-memory caching | Performance optimization, caching strategies |
| **Amazon SageMaker** | ML model hosting | Machine learning deployment, model serving |
| **Amazon Lambda** | Serverless functions | Event-driven programming, serverless architecture |
| **Amazon API Gateway** | REST API management | API design, rate limiting, authentication |
| **Amazon S3** | Data lake storage | Data lake architecture, object storage |
| **Amazon CloudWatch** | Monitoring & logging | Observability, metrics, alarms |
| **Amazon VPC** | Networking | Network security, subnets, routing |
| **Amazon EC2** | Compute instances | Infrastructure management, auto-scaling |

## 📊 Features

### **Real-time Analytics**
- Live cryptocurrency price streaming from CoinGecko API
- Real-time price updates every 60 seconds
- Interactive charts and visualizations
- Market overview with total market cap and volume

### **Machine Learning**
- SageMaker-powered price predictions
- Real-time ML model inference
- Confidence scoring for predictions
- Historical data analysis

### **Microservices Architecture**
- FastAPI backend with RESTful APIs
- React frontend with Material-UI
- API Gateway for request routing
- Lambda functions for data processing

### **AWS Best Practices**
- Infrastructure as Code with Terraform
- Security groups and IAM roles
- CloudWatch monitoring and logging
- Auto-scaling and high availability

## 🛠️ Quick Start

### **Prerequisites**
- AWS CLI configured
- Terraform installed
- Python 3.8+
- Node.js 16+

### **Deploy Everything**
```bash
# Clone the repository
git clone <repository-url>
cd aws-crypto-analytics

# Make scripts executable
chmod +x deploy.sh stop.sh

# Deploy the entire platform
./deploy.sh dev us-east-1
```

### **Access the Application**
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
└── SETUP.md               # Detailed setup guide
```

## 🎨 Dashboard Features

### **Real-time Dashboard**
- Live cryptocurrency price cards with color-coded changes
- Market overview with total market cap and volume
- Interactive price charts using Recharts
- Top gainers and losers tracking

### **ML Predictions**
- SageMaker-powered price predictions
- Confidence scoring for each prediction
- Historical data analysis
- Real-time model inference

### **AWS Service Status**
- Real-time status of all AWS services
- Service health indicators
- Performance metrics display

## 🔧 Manual Setup

For step-by-step setup, see [SETUP.md](SETUP.md)

## 🧹 Cleanup

To stop all services and clean up:

```bash
./stop.sh
```

  ## 📈 Production Deployment
  
  For production deployment:
  
  1. **Use AWS ECS/EKS** for containerized deployment
  2. **Set up CI/CD** with GitHub Actions
  3. **Configure auto-scaling** for all services
  4. **Implement security** with AWS WAF and Shield
  5. **Use CloudFront** for global content delivery

## 🎯 Job Interview Benefits

This project demonstrates:

### **Technical Skills**
- ✅ AWS service integration
- ✅ Microservices architecture
- ✅ Real-time data processing
- ✅ Machine learning deployment
- ✅ Infrastructure as Code
- ✅ API design and development

### **AWS Expertise**
- ✅ Kinesis Data Streams
- ✅ DynamoDB
- ✅ ElastiCache Redis
- ✅ SageMaker
- ✅ Lambda
- ✅ API Gateway
- ✅ S3
- ✅ CloudWatch
- ✅ VPC and networking

### **Best Practices**
- ✅ Security and IAM
- ✅ Monitoring and logging
- ✅ Auto-scaling
- ✅ High availability
- ✅ Cost optimization

## 📊 Monitoring

### **CloudWatch Dashboards**
- Lambda function metrics
- Kinesis stream monitoring
- DynamoDB performance
- API Gateway metrics

### **Local Logs**
- `data-pipeline/producer.log` - Kinesis producer logs
- `backend/backend.log` - FastAPI server logs
- `frontend/frontend.log` - React development logs

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more AWS services
- Implementing additional ML models
- Improving the UI/UX
- Adding more data sources
- Implementing authentication
- Adding more analytics features

## 📚 Learning Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
