import boto3
from botocore.exceptions import ClientError
client = boto3.client('cloudformation')

def create_wait_stack(stack_name):
    waiter = client.get_waiter('stack_delete_complete')
    try:
        waiter.wait(StackName=stack_name)
    except ClientError as e:
        print('[ERROR] Failed to delete stack [ Name = %s ]' % stack_name)
        print('[REASON] %s' % e)
        return False
    else:
        print('[SUCCESS] The stack was deleted successfully [ Name = %s ]' % stack_name)
        return True

if __name__=='__main__':
    import delete_stack
    create_wait_stack(delete_stack.stack_name)