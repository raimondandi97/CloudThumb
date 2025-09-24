provider "aws" {
  region = "us-east-1"
}

# Create an S3 bucket
resource "aws_s3_bucket" "example" {
  bucket = "cloud-thumb-bucket"
}

resource "aws_dynamodb_table" "example" {
  name           = "CloudThumb-Table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"  # String
  }

  tags = {
    Environment = "dev"
    Project     = "CloudThumb"
  }
}

resource "aws_ecr_repository" "lambda_repo" {
  name = "cloudthumb-lambda-repo"
}

resource "aws_iam_role" "lambda_role" {
  name = "cloudthumb_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "opencv_lambda" {
  function_name = "opencv_lambda"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = ""
}
