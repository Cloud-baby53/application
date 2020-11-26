import boto3
from botocore.exceptions import ClientError

client = boto3.client('cloudformation')
stack_name = 'test'
parameters = []
with open('./template.yaml') as template:
    template = template.read()

def create_stack(stack_name, template, parameters):
    try:
        response = client.create_stack(
            StackName=stack_name,
            TemplateBody=template,
            Parameters=parameters,
            Capabilities=[
                'CAPABILITY_IAM',
                'CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND',
            ]
        )
        return True
    except ClientError as e:
        return False
result = create_stack(stack_name, template, parameters)
print(result)