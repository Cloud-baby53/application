#lambda_function.py
Extract the performance optimal API from the marketplace and automatically register it in the DynamoDB record.
The execution interval is called every minute with CloudWatchEvents, and the processing in the Lambda function is looped 3 times at 15s intervals to reproduce the periodic execution every 20 seconds.

#update_dynamodb.zip
You can achieve this by uploading this zip file to your lambda function.

※Precautions when creating a lambda function
・Specify python3.6 for runtime
・Timeout time set to 1 minute
・Memory should be set to 192MB