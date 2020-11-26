from template import main
import argparse

def deploy():
    def read_template(filepath):
        with open(filepath) as template:
            return template.read()
            
    stack_name = 'test'
    parameters = []
    template = read_template('template/template.yaml')
    result = main.deploy(stack_name, template, parameters)
    if result == False:
        return False
    
    stack_name = 'test1'
    parameters = []
    template = read_template('template/template1.yaml')
    result = main.deploy(stack_name, template, parameters)
    
    return result
        
def delete():
    stack_name = 'test1'
    result = main.delete(stack_name)
    if result == False:
        return False
    
    stack_name = 'test'
    result = main.delete(stack_name)
    
    return result

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--flag')
    args = parser.parse_args()
    if args.flag == 'create':
        result = deploy()
        print(result)
    elif args.flag == 'delete':
        result = delete()
        print(result)
    else:
        print('Please enter the correct argument [ --flag create or delete ]')
    
    