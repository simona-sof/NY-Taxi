resource "aws_s3_bucket" "taxi_bucket" {
  bucket = "my-taxi-bucket-1"
  tags = {
    Name        = "NYTaxiBucket"
    Environment = "Analysis"
  }
}