# NYC Taxi Data Pipeline

This project processes and transforms NYC taxi trip data using **PySpark**. It reads taxi trip data from a Parquet file, calculates journey lengths and tip percentages, and then writes the results to an S3 bucket. The project also integrates with **AWS Secrets Manager** to securely access S3 credentials. Terraform files are provided to set up the necessary AWS infrastructure.

## Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Disclaimer](#disclaimer)

## Instalation

1. Clone the repository
```bash
git clone https://github.com/yourusername/taxi-data-transformation.git
cd taxi-data-transformation
```
2. Install dependencies

- Install required libraries
```bash
pip install -r requirements.txt
```
- Have Terraform installed: Follow the [Terraform installation guide](https://learn.hashicorp.com/tutorials/terraform/install-cli).

3. Set up AWS infrastructure
- Initialise Terraform
```bash
terraform init
```
- Create execution plan
```bash
terraform plan
```
- Apply Terraform Configuration to Provision S3 Bucket and IAM User:
```bash
terraform apply
```
- Terraform Output: After applying, Terraform will output the S3 bucket name and access key for the IAM user, add the access key to your environment:
```bash
export access_key=<your_aws_access_key>
```

## Usage 
Add the NYC Taxi data you want to transform to data/ folder and run the PySpark job:
```bash
python3 transformation.py
```
The output will be saved to AWS S3 bucket as a Parquet file.

## Disclaimer
This code is provided "as is" without any warranties or guarantees of performance. 
The authors are not responsible for any issues or damages resulting from the use of this code. Any updates or improvements will be shared through this GitHub repository.
