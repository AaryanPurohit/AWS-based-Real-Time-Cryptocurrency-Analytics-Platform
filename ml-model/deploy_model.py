#!/usr/bin/env python3
"""
AWS SageMaker ML Model Deployment Script
Deploys a cryptocurrency price prediction model to SageMaker
Demonstrates ML model deployment and AWS SageMaker integration
"""

import boto3
import argparse
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoMLModel:
    """
    Cryptocurrency price prediction model using AWS SageMaker
    Demonstrates ML model training and deployment
    """
    
    def __init__(self, environment: str, region: str):
        """
        Initialize the ML model deployment
        
        Args:
            environment: Deployment environment
            region: AWS region
        """
        self.environment = environment
        self.region = region
        self.sagemaker = boto3.client('sagemaker', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        
        # Model configuration
        self.model_name = f"crypto-prediction-model-{environment}"
        self.endpoint_name = f"crypto-prediction-endpoint-{environment}"
        self.bucket_name = f"crypto-ml-models-{environment}"
        
        logger.info(f"Initialized ML model deployment for environment: {environment}")
    
    def create_s3_bucket(self):
        """Create S3 bucket for model artifacts"""
        try:
            self.s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
            logger.info(f"Created S3 bucket: {self.bucket_name}")
        except self.s3.exceptions.BucketAlreadyExists:
            logger.info(f"S3 bucket {self.bucket_name} already exists")
        except Exception as e:
            logger.error(f"Error creating S3 bucket: {e}")
            raise
    
    def generate_training_data(self) -> pd.DataFrame:
        """
        Generate synthetic training data for the model
        In a real scenario, this would use historical cryptocurrency data
        """
        logger.info("Generating training data...")
        
        # Generate synthetic data for demonstration
        np.random.seed(42)
        n_samples = 1000
        
        # Features: price, volume, market_cap, price_change
        price = np.random.uniform(1000, 50000, n_samples)
        volume = np.random.uniform(1000000, 100000000, n_samples)
        market_cap = price * np.random.uniform(1000000, 10000000, n_samples)
        price_change = np.random.uniform(-20, 20, n_samples)
        
        # Target: next period price (with some correlation to features)
        next_price = price * (1 + price_change/100 + np.random.normal(0, 0.05, n_samples))
        
        # Create DataFrame
        data = pd.DataFrame({
            'price': price,
            'volume': volume,
            'market_cap': market_cap,
            'price_change': price_change,
            'next_price': next_price
        })
        
        logger.info(f"Generated {len(data)} training samples")
        return data
    
    def train_model(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Train the ML model
        
        Args:
            data: Training data
            
        Returns:
            Dictionary containing model and scaler
        """
        logger.info("Training ML model...")
        
        # Prepare features and target
        features = ['price', 'volume', 'market_cap', 'price_change']
        X = data[features]
        y = data['next_price']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_scaled, y)
        
        # Save model artifacts
        model_path = f"model_{self.environment}"
        os.makedirs(model_path, exist_ok=True)
        
        joblib.dump(model, f"{model_path}/model.pkl")
        joblib.dump(scaler, f"{model_path}/scaler.pkl")
        
        # Save feature names
        with open(f"{model_path}/features.json", 'w') as f:
            json.dump(features, f)
        
        logger.info("Model training completed")
        
        return {
            'model': model,
            'scaler': scaler,
            'features': features,
            'model_path': model_path
        }
    
    def upload_model_to_s3(self, model_path: str):
        """
        Upload model artifacts to S3
        
        Args:
            model_path: Path to model artifacts
        """
        logger.info("Uploading model to S3...")
        
        for file_name in os.listdir(model_path):
            file_path = os.path.join(model_path, file_name)
            s3_key = f"models/{self.model_name}/{file_name}"
            
            self.s3.upload_file(file_path, self.bucket_name, s3_key)
            logger.info(f"Uploaded {file_name} to s3://{self.bucket_name}/{s3_key}")
    
    def create_sagemaker_model(self):
        """Create SageMaker model"""
        logger.info("Creating SageMaker model...")
        
        # Model artifact location
        model_data_url = f"s3://{self.bucket_name}/models/{self.model_name}/model.tar.gz"
        
        # Create model
        response = self.sagemaker.create_model(
            ModelName=self.model_name,
            PrimaryContainer={
                'Image': '763104351884.dkr.ecr.us-east-1.amazonaws.com/sklearn:1.0-1-cpu-py3',
                'ModelDataUrl': model_data_url,
                'Environment': {
                    'SAGEMAKER_PROGRAM': 'inference.py',
                    'SAGEMAKER_SUBMIT_DIRECTORY': '/opt/ml/code',
                    'SAGEMAKER_CONTAINER_LOG_LEVEL': '20',
                    'SAGEMAKER_REGION': self.region
                }
            },
            ExecutionRoleArn=self._get_or_create_role()
        )
        
        logger.info(f"Created SageMaker model: {self.model_name}")
        return response
    
    def create_endpoint(self):
        """Create SageMaker endpoint"""
        logger.info("Creating SageMaker endpoint...")
        
        # Create endpoint configuration
        config_name = f"{self.endpoint_name}-config"
        
        self.sagemaker.create_endpoint_config(
            EndpointConfigName=config_name,
            ProductionVariants=[
                {
                    'VariantName': 'default',
                    'ModelName': self.model_name,
                    'InitialInstanceCount': 1,
                    'InstanceType': 'ml.t3.medium'
                }
            ]
        )
        
        # Create endpoint
        self.sagemaker.create_endpoint(
            EndpointName=self.endpoint_name,
            EndpointConfigName=config_name
        )
        
        logger.info(f"Creating endpoint: {self.endpoint_name}")
        
        # Wait for endpoint to be ready
        self._wait_for_endpoint()
        
        return self.endpoint_name
    
    def _wait_for_endpoint(self):
        """Wait for endpoint to be in service"""
        logger.info("Waiting for endpoint to be ready...")
        
        while True:
            response = self.sagemaker.describe_endpoint(EndpointName=self.endpoint_name)
            status = response['EndpointStatus']
            
            if status == 'InService':
                logger.info("Endpoint is ready!")
                break
            elif status == 'Failed':
                raise Exception("Endpoint creation failed")
            else:
                logger.info(f"Endpoint status: {status}")
                time.sleep(30)
    
    def _get_or_create_role(self) -> str:
        """Get or create IAM role for SageMaker"""
        # In a real deployment, you would create a proper IAM role
        # For this demo, we'll use a placeholder
        return "arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole-20231201T000000"
    
    def test_endpoint(self):
        """Test the deployed endpoint"""
        logger.info("Testing endpoint...")
        
        # Create runtime client
        runtime = boto3.client('sagemaker-runtime', region_name=self.region)
        
        # Test data
        test_data = {
            'symbol': 'BTC',
            'features': [
                {
                    'price': 45000.0,
                    'volume': 25000000000.0,
                    'market_cap': 850000000000.0,
                    'price_change': 2.5
                }
            ],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            response = runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(test_data)
            )
            
            result = json.loads(response['Body'].read().decode())
            logger.info(f"Test prediction: {result}")
            
        except Exception as e:
            logger.error(f"Error testing endpoint: {e}")
            raise
    
    def deploy(self):
        """Deploy the complete ML model"""
        logger.info("Starting ML model deployment...")
        
        try:
            # Create S3 bucket
            self.create_s3_bucket()
            
            # Generate training data
            data = self.generate_training_data()
            
            # Train model
            model_artifacts = self.train_model(data)
            
            # Upload to S3
            self.upload_model_to_s3(model_artifacts['model_path'])
            
            # Create SageMaker model
            self.create_sagemaker_model()
            
            # Create endpoint
            endpoint_name = self.create_endpoint()
            
            # Test endpoint
            self.test_endpoint()
            
            logger.info("ML model deployment completed successfully!")
            
            return {
                'model_name': self.model_name,
                'endpoint_name': endpoint_name,
                'bucket_name': self.bucket_name
            }
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            raise

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description='Deploy ML model to SageMaker')
    parser.add_argument('--environment', default='dev', help='Deployment environment')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    
    args = parser.parse_args()
    
    # Create and deploy model
    model = CryptoMLModel(args.environment, args.region)
    result = model.deploy()
    
    print(f"\n🎉 ML Model Deployment Complete!")
    print(f"Model Name: {result['model_name']}")
    print(f"Endpoint Name: {result['endpoint_name']}")
    print(f"S3 Bucket: {result['bucket_name']}")
    print(f"Environment: {args.environment}")
    print(f"Region: {args.region}")

if __name__ == "__main__":
    main() 