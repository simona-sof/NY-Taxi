resource "aws_iam_policy" "taxi_bucket_policy" {
    name = "taxi-bucket-policy"
    description = "Allow access to S3 bucket"
    policy = jsonncode({
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
resource "aws_iam_policy_attachment" "attach_bucket_policy" {
    name = "taxi-bucket-policy-attachment"
    role = aws_iam_role.taxi_bucket_policy.name
    arn = aws_iam_policy.taxi_bucket_policy.arn
}