import boto3
from botocore.exceptions import ClientError

client = boto3.client('cloudformation')
stack_name = 'test'

def check_stack_ststus(stack_name):
    try:
        response = client.describe_stacks(
            StackName='test',
        )['Stacks'][0]['StackStatus']
    except ClientError as e:
        return False
    else:
        if response == 'CREATE_COMPLETE':
            return True
        else:
            return False

result = check_stack_ststus(stack_name)
print(result)
