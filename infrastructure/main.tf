# AWS Real-Time Cryptocurrency Analytics Platform - Infrastructure as Code
# This demonstrates advanced AWS service integration and microservices architecture

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr = var.vpc_cidr
  environment = var.environment
}

# Kinesis Data Streams for real-time data processing
resource "aws_kinesis_stream" "crypto_stream" {
  name             = "crypto-price-stream-${var.environment}"
  shard_count      = 2
  retention_period = 24

  tags = {
    Environment = var.environment
    Project     = "crypto-analytics"
  }
}

# DynamoDB for real-time data storage
resource "aws_dynamodb_table" "crypto_prices" {
  name           = "crypto-prices-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "symbol"
  range_key      = "timestamp"

  attribute {
    name = "symbol"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Environment = var.environment
    Project     = "crypto-analytics"
  }
}

# ElastiCache Redis for caching
resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "redis-subnet-group-${var.environment}"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_parameter_group" "redis_params" {
  family = "redis7"
  name   = "redis-params-${var.environment}"
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "crypto-redis-${var.environment}"
  description                = "Redis cluster for crypto analytics"
  node_type                  = "cache.t3.micro"
  port                       = 6379
  parameter_group_name       = aws_elasticache_parameter_group.redis_params.name
  subnet_group_name          = aws_elasticache_subnet_group.redis_subnet_group.name
  security_group_ids         = [aws_security_group.redis.id]
  automatic_failover_enabled = false
  num_cache_clusters         = 1

  tags = {
    Environment = var.environment
    Project     = "crypto-analytics"
  }
}

# S3 Bucket for data lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "crypto-data-lake-${var.environment}-${random_string.bucket_suffix.result}"
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake_private" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lambda function for data processing
resource "aws_lambda_function" "data_processor" {
  filename         = "../backend/lambda_function.zip"
  function_name    = "crypto-data-processor-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.crypto_prices.name
      KINESIS_STREAM = aws_kinesis_stream.crypto_stream.name
      REDIS_ENDPOINT = aws_elasticache_replication_group.redis.primary_endpoint_address
    }
  }

  tags = {
    Environment = var.environment
    Project     = "crypto-analytics"
  }
}

# API Gateway for REST API
resource "aws_api_gateway_rest_api" "crypto_api" {
  name = "crypto-analytics-api-${var.environment}"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "prices" {
  rest_api_id = aws_api_gateway_rest_api.crypto_api.id
  parent_id   = aws_api_gateway_rest_api.crypto_api.root_resource_id
  path_part   = "prices"
}

resource "aws_api_gateway_method" "get_prices" {
  rest_api_id   = aws_api_gateway_rest_api.crypto_api.id
  resource_id   = aws_api_gateway_resource.prices.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.crypto_api.id
  resource_id = aws_api_gateway_resource.prices.id
  http_method = aws_api_gateway_method.get_prices.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.data_processor.invoke_arn
}

# CloudWatch for monitoring
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.data_processor.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "crypto-analytics-dashboard-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6

        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", aws_lambda_function.data_processor.function_name],
            [".", "Invocations", ".", "."],
            [".", "Errors", ".", "."]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "Lambda Performance"
        }
      }
    ]
  })
}

# IAM roles and policies
resource "aws_iam_role" "lambda_role" {
  name = "crypto-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "lambda-dynamodb-policy-${var.environment}"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.crypto_prices.arn
      }
    ]
  })
}

# Security Groups
resource "aws_security_group" "redis" {
  name_prefix = "redis-${var.environment}"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "redis-sg-${var.environment}"
    Environment = var.environment
  }
}

# Random string for unique bucket names
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

# Outputs
output "kinesis_stream_name" {
  value = aws_kinesis_stream.crypto_stream.name
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.crypto_prices.name
}

output "redis_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "api_gateway_url" {
  value = "${aws_api_gateway_rest_api.crypto_api.execution_arn}/prices"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.data_lake.bucket
} 