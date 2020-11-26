import boto3
from botocore.exceptions import ClientError

client = boto3.client('cloudformation')
stack_name = 'test1'

def delete_stack(stack_name):
    try:
        response = client.delete_stack(
            StackName=stack_name
        )
        print('[INFO] Delete Stack Start [ Name = %s ]' % stack_name)
        return True
    except ClientError as e:
        print('[ERROR] Failed to start stack creation [ Name = %s ]' % stack_name)
        print('[REASON] %s' % e)
        return False
        
result = delete_stack(stack_name)
print(result)