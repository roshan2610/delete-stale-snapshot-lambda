# delete-stale-snapshot-lambda
Created a Lambda function to identify and delete stale EBS snapshots, reducing storage costs in AWS.
Utilized AWS Lambda, EC2, and Boto3 SDK for Python.
Automated the process to optimize storage resources and minimize unnecessary costs.

Steps - 
1. Create a Lambda function in AWS
2. Give required IAM permissions to the role eg. DescribeSnapshots, DescribeInstances, DescribeVolumes, DeleteSnapshot
3. Deploy the lambda function
4. Test the function
5. To run this function you could create a rule in CloudWatch as well.
