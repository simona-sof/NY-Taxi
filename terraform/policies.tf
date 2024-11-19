resource "aws_iam_user" "s3_access_user" {
  name = "s3-user"
}

resource "aws_iam_access_key" "s3_user_access_key" {
  user = aws_iam_user.s3_access_user.name
}

resource "aws_iam_policy" "taxi_bucket_policy" {
  name        = "taxi-bucket-policy"
  description = "Allow access to S3 bucket"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ],
        "Resource" : [
          aws_s3_bucket.taxi_bucket.arn,
          "${aws_s3_bucket.taxi_bucket.arn}/*"
        ]
      }
    ]
  })
}
resource "aws_iam_user_policy_attachment" "attach_bucket_policy" {
  user       = aws_iam_user.s3_access_user.name
  policy_arn = aws_iam_policy.taxi_bucket_policy.arn
}

output "s3_user_access_key_id" {
  value = aws_iam_access_key.s3_user_access_key.id
}

output "s3_user_secret_access_key" {
  value     = aws_iam_access_key.s3_user_access_key.secret
  sensitive = true
}

resource "aws_secretsmanager_secret" "s3_user_secret" {
  name = aws_iam_user.s3_access_user.name
}

resource "aws_secretsmanager_secret_version" "s3_user_secret_version" {
  secret_id     = aws_iam_user.s3_access_user.name
  secret_string = aws_iam_access_key.s3_user_access_key.secret
}