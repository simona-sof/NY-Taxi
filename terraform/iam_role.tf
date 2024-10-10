resource "aws_iam_role" "s3_access_role" {
    name = "s3-access-role"
    assume_role_policy = jsonncode({
        "Version" : "2012-10-17",
        "Statement" : [{
            "Effect" : "Allow",
            "Action" : "sts:AssumeRole",
            Principal = {
                "Service" : "ec2.amazonaws.com"
            }
        }]
    })
}