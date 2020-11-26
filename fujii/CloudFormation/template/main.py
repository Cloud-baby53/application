import boto3
from botocore.exceptions import ClientError

client = boto3.client('cloudformation')
    
def deploy(stack_name, template, parameters):
    def create_stack(stack_name, template, parameters):
        try:
            response = client.create_stack(
                StackName=stack_name,
                TemplateBody=template,
                Parameters=parameters,
                Capabilities=[
                    'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND'
                ]
            )
            print('[INFO] Create Stack Start [ Name = %s ]' % stack_name)
        except ClientError as e:
            if e.response['Error']['Code'] == "AlreadyExistsException":
                if check_stack_status(stack_name) == True:
                    return True
                else:
                    return False
            else:
                print('[ERROR] Failed to start stack creation [ Name = %s ]' % stack_name)
                print('[REASON] %s' % e)
                return False
        else:
            return create_wait_stack(stack_name)
            
    
    def create_wait_stack(stack_name):
        waiter = client.get_waiter('stack_create_complete')
        try:
            waiter.wait(StackName=stack_name)
        except ClientError as e:
            print('[ERROR] Failed to create stack [ Name = %s ]' % stack_name)
            print('[REASON] %s' % e)
            return False
        else:
            print('[SUCCESS] The stack was created successfully [ Name = %s ]' % stack_name)
            return True
        
    def check_stack_status(stack_name):
        try:
            response = client.describe_stacks(
                StackName=stack_name,
            )['Stacks'][0]['StackStatus']
        except ClientError as e:
            return False
        else:
            if response == 'CREATE_COMPLETE':
                print('[SUCCESS] Stack is already exists & Status is Completed [ Name = %s ]' % stack_name)
                return True
            else:
                print('[ERROR] Stack is already exists & Status isn\'t Completed [ Name = %s ]' % stack_name)
                return False

    ################## main process #######################
    return create_stack(stack_name, template, parameters)
    ####################################################### 

def delete(stack_name):
    def delete_stack(stack_name):
        try:
            response = client.delete_stack(
                StackName=stack_name
            )
            print('[INFO] Delete Stack Start [ Name = %s ]' % stack_name)
        except ClientError as e:
            print('[ERROR] Failed to start stack deletion [ Name = %s ]' % stack_name)
            print('[REASON] %s' % e)
            return False
        else:
            return delete_wait_stack(stack_name)
    
    def delete_wait_stack(stack_name):
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
            
    ################## main process #######################       
    return delete_stack(stack_name)
    ####################################################### 