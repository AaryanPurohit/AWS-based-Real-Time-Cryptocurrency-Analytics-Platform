# 🚀 Complete AWS Setup Guide for Beginners

## Welcome to AWS! 🌟

This guide will walk you through setting up AWS from scratch and deploying the Crypto Analytics Platform. Even if you've never used AWS before, you'll be able to follow along!

## 📋 What You'll Learn

By the end of this guide, you'll know how to:
- ✅ Create an AWS account
- ✅ Set up AWS CLI
- ✅ Use AWS services (Kinesis, DynamoDB, SageMaker, etc.)
- ✅ Deploy infrastructure with Terraform
- ✅ Run a complete real-time analytics platform

---

## 🎯 Step 1: Create Your AWS Account

### 1.1 Sign Up for AWS
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Enter your email address
4. Choose "Personal Account" (free tier available)

### 1.2 Account Details
- **Account Name**: Your name or company name
- **Email**: Use a real email (you'll need to verify it)
- **Password**: Create a strong password

### 1.3 Contact Information
- Fill in your contact details
- Select "Personal" account type
- Click "Continue"

### 1.4 Payment Information
- **Credit Card**: You'll need a valid credit card
- **Billing Address**: Your real billing address
- **Note**: AWS Free Tier gives you $0 usage for 12 months!

### 1.5 Identity Verification
- AWS will call your phone number
- Enter the 4-digit code they provide
- Click "Continue"

### 1.6 Choose Support Plan
- Select "Free" plan (Basic support)
- Click "Complete sign up"

**🎉 Congratulations! You now have an AWS account!**

---

## 🎯 Step 2: Set Up AWS CLI

### 2.1 Install AWS CLI

**On macOS (using Homebrew):**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install AWS CLI
brew install awscli
```

**On macOS (manual install):**
```bash
# Download AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"

# Install
sudo installer -pkg AWSCLIV2.pkg -target /
```

**On Windows:**
1. Download from: https://aws.amazon.com/cli/
2. Run the installer
3. Follow the installation wizard

### 2.2 Verify Installation
```bash
aws --version
```
You should see something like: `aws-cli/2.x.x`

---

## 🎯 Step 3: Create AWS Access Keys

### 3.1 Log into AWS Console
1. Go to [console.aws.amazon.com](https://console.aws.amazon.com)
2. Sign in with your email and password

### 3.2 Navigate to IAM
1. In the search bar, type "IAM"
2. Click on "IAM" (Identity and Access Management)

### 3.3 Create a User
1. Click "Users" in the left sidebar
2. Click "Create user"
3. **User name**: `crypto-analytics-user`
4. Check "Access key - Programmatic access"
5. Click "Next: Permissions"

### 3.4 Attach Permissions
1. Click "Attach existing policies directly"
2. Search for and select these policies:
   - `AmazonKinesisFullAccess`
   - `AmazonDynamoDBFullAccess`
   - `AmazonElastiCacheFullAccess`
   - `AmazonSageMakerFullAccess`
   - `AmazonS3FullAccess`
   - `AWSLambda_FullAccess`
   - `AmazonAPIGatewayInvokeFullAccess`
   - `CloudWatchFullAccess`
   - `AmazonVPCFullAccess`
   - `AmazonEC2FullAccess`
3. Click "Next: Tags"
4. Click "Next: Review"
5. Click "Create user"

### 3.5 Get Your Access Keys
1. Click on your new user
2. Click "Security credentials" tab
3. Click "Create access key"
4. Choose "Application running outside AWS"
5. Click "Next"
6. **IMPORTANT**: Copy both the Access Key ID and Secret Access Key
7. Click "Create access key"

**⚠️ Save these keys securely! You won't see the secret key again!**

---

## 🎯 Step 4: Configure AWS CLI

### 4.1 Set Up Credentials
```bash
aws configure
```

When prompted, enter:
- **AWS Access Key ID**: Your access key from step 3.5
- **AWS Secret Access Key**: Your secret key from step 3.5
- **Default region name**: `us-east-1`
- **Default output format**: `json`

### 4.2 Test Your Configuration
```bash
aws sts get-caller-identity
```

You should see your account ID and user ARN.

---

## 🎯 Step 5: Install Required Software

### 5.1 Install Terraform

**On macOS:**
```bash
brew install terraform
```

**On Windows:**
1. Download from: https://www.terraform.io/downloads
2. Extract to a folder
3. Add the folder to your PATH

**On Linux:**
```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```

### 5.2 Verify Terraform
```bash
terraform --version
```

### 5.3 Install Python (if not already installed)
```bash
# Check if Python is installed
python3 --version

# If not installed, on macOS:
brew install python3
```

### 5.4 Install Node.js (if not already installed)
```bash
# Check if Node.js is installed
node --version

# If not installed, on macOS:
brew install node
```

---

## 🎯 Step 6: Understand AWS Services

Before we deploy, let's understand what each AWS service does:

### 6.1 Amazon Kinesis Data Streams
- **What it does**: Real-time data streaming
- **Our use**: Stream cryptocurrency prices from CoinGecko API
- **Think of it**: Like a real-time pipeline for data

### 6.2 Amazon DynamoDB
- **What it does**: NoSQL database for real-time data
- **Our use**: Store cryptocurrency prices and market data
- **Think of it**: Like a super-fast spreadsheet in the cloud

### 6.3 Amazon ElastiCache Redis
- **What it does**: In-memory caching
- **Our use**: Cache frequently accessed data for speed
- **Think of it**: Like a super-fast memory bank

### 6.4 Amazon SageMaker
- **What it does**: Machine learning platform
- **Our use**: Predict cryptocurrency prices
- **Think of it**: Like a smart AI brain in the cloud

### 6.5 Amazon Lambda
- **What it does**: Serverless functions
- **Our use**: Process data from Kinesis streams
- **Think of it**: Like tiny programs that run only when needed

### 6.6 Amazon S3
- **What it does**: Object storage
- **Our use**: Store data lake and ML models
- **Think of it**: Like a massive hard drive in the cloud

---

## 🎯 Step 7: Deploy the Infrastructure

### 7.1 Navigate to Project
```bash
cd aws-crypto-analytics
```

### 7.2 Initialize Terraform
```bash
cd infrastructure
terraform init
```

### 7.3 Plan the Deployment
```bash
terraform plan -var="environment=dev" -var="aws_region=us-east-1"
```

This will show you what AWS resources will be created.

### 7.4 Deploy Infrastructure
```bash
terraform apply -var="environment=dev" -var="aws_region=us-east-1" -auto-approve
```

**This will take 5-10 minutes to create all AWS resources.**

### 7.5 Check What Was Created
```bash
terraform output
```

You should see:
- Kinesis stream name
- DynamoDB table name
- Redis endpoint
- S3 bucket name

---

## 🎯 Step 8: Deploy the ML Model

### 8.1 Install ML Dependencies
```bash
cd ../ml-model
pip install -r requirements.txt
```

### 8.2 Deploy ML Model
```bash
python deploy_model.py --environment dev --region us-east-1
```

**This will take 10-15 minutes to train and deploy the ML model.**

---

## 🎯 Step 9: Start the Data Pipeline

### 9.1 Install Pipeline Dependencies
```bash
cd ../data-pipeline
pip install -r requirements.txt
```

### 9.2 Set Environment Variables
```bash
export KINESIS_STREAM_NAME=crypto-price-stream-dev
export AWS_REGION=us-east-1
export FETCH_INTERVAL=60
```

### 9.3 Start Data Producer
```bash
python kinesis_producer.py
```

You should see logs showing data being fetched and sent to Kinesis.

---

## 🎯 Step 10: Start the Backend

### 10.1 Install Backend Dependencies
```bash
cd ../backend
pip install -r requirements.txt
```

### 10.2 Set Environment Variables
```bash
export DYNAMODB_TABLE=crypto-prices-dev
export REDIS_ENDPOINT=your-redis-endpoint-from-terraform-output
export S3_BUCKET=your-s3-bucket-from-terraform-output
```

### 10.3 Start Backend Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 10.4 Test the API
Open a new terminal and run:
```bash
curl http://localhost:8000/health
```

You should see a JSON response with service status.

---

## 🎯 Step 11: Start the Frontend

### 11.1 Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 11.2 Start Frontend Server
```bash
npm start
```

Your browser should automatically open to `http://localhost:3000`

---

## 🎯 Step 12: Access Your Application

### 12.1 Frontend Dashboard
- **URL**: http://localhost:3000
- **What you'll see**: Real-time cryptocurrency dashboard
- **Features**: Live price updates, charts, ML predictions

### 12.2 Backend API
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 12.3 API Endpoints
- `GET /api/prices` - Get all cryptocurrency prices
- `GET /api/prices/{symbol}` - Get specific cryptocurrency
- `GET /api/analytics/market` - Get market analytics
- `POST /api/predict` - Get ML predictions

---

## 🎯 Step 13: Monitor Your Resources

### 13.1 AWS Console Monitoring
1. Go to [console.aws.amazon.com](https://console.aws.amazon.com)
2. Navigate to different services to see your resources:
   - **Kinesis**: Search "Kinesis" → Data Streams
   - **DynamoDB**: Search "DynamoDB" → Tables
   - **SageMaker**: Search "SageMaker" → Endpoints
   - **S3**: Search "S3" → Buckets

### 13.2 CloudWatch Monitoring
1. Search "CloudWatch" in AWS Console
2. Click "Dashboards"
3. You should see your custom dashboard

---

## 🎯 Step 14: Understanding Costs

### 14.1 AWS Free Tier
- **DynamoDB**: 25 GB storage, 25 WCU/RCU
- **Lambda**: 1M requests/month
- **S3**: 5 GB storage
- **Kinesis**: 2 shard hours/day
- **SageMaker**: Limited free tier

### 14.2 Estimated Monthly Costs (Free Tier)
- **Development**: $0-5/month
- **Production**: $50-200/month (depending on usage)

### 14.3 Cost Monitoring
1. Go to AWS Console
2. Search "Billing"
3. Click "Bills" to see your charges

---

## 🎯 Step 15: Cleanup

### 15.1 Stop All Services
```bash
# Stop data pipeline (Ctrl+C)
# Stop backend (Ctrl+C)
# Stop frontend (Ctrl+C)
```

### 15.2 Destroy Infrastructure
```bash
cd infrastructure
terraform destroy -auto-approve
```

**⚠️ This will delete all AWS resources and stop billing!**

---

## 🎯 Troubleshooting

### Common Issues:

#### 1. AWS Credentials Error
```bash
aws configure
# Re-enter your access keys
```

#### 2. Terraform State Issues
```bash
cd infrastructure
terraform init -reconfigure
```

#### 3. Port Already in Use
```bash
# Check what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Kill the process
kill -9 <PID>
```

#### 4. Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Node.js Dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 Next Steps

### 1. Learn More AWS Services
- **ECS/EKS**: Container orchestration
- **CloudFront**: Content delivery
- **RDS**: Relational databases
- **Elasticsearch**: Search and analytics

### 2. Enhance the Project
- Add user authentication
- Implement more ML models
- Add more data sources
- Create mobile app

### 3. Production Deployment
- Set up CI/CD pipelines
- Configure auto-scaling
- Implement monitoring and alerts
- Add security measures

---

## 🎯 AWS Best Practices

### 1. Security
- Use IAM roles instead of access keys
- Enable MFA on your AWS account
- Use VPC for network isolation
- Encrypt data at rest and in transit

### 2. Cost Optimization
- Use AWS Cost Explorer
- Set up billing alerts
- Use reserved instances for production
- Monitor and optimize resource usage

### 3. Monitoring
- Set up CloudWatch alarms
- Use AWS X-Ray for tracing
- Implement proper logging
- Monitor application metrics

---

## 🎯 Congratulations! 🎉

You've successfully:
- ✅ Created an AWS account
- ✅ Set up AWS CLI
- ✅ Deployed infrastructure with Terraform
- ✅ Deployed ML models to SageMaker
- ✅ Built a real-time data pipeline
- ✅ Created a full-stack application
- ✅ Demonstrated multiple AWS services

**You now have hands-on experience with 10+ AWS services! This is exactly the kind of project that impresses hiring managers.** 🚀

---

## 📚 Additional Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

**Good luck with your AWS journey! 🌟** 