import boto3
client = boto3.client('cloudformation')

def create_wait_stack(stack_name):
    waiter = client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)

if __name__=='__main__':
    import create_stack
    create_wait_stack(create_stack.stack_name)
    