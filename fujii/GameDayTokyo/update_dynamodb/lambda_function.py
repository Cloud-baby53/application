import pandas as pd
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

team_name = 'team2'
table_name = 'service-table'
url = 'http://original20010207.s3-website.us-east-2.amazonaws.com/'
service_type_list = ['swapcaser', 'leeter', 'reverser']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
    
def lambda_handler(event, context): 
    table_data = get_table_html(url)
    endpoint_list = get_optimized_endpoint(table_data)
    delete_key_list = get_delete_key()
    put_new_endpoint(endpoint_list, delete_key_list)
    
def get_table_html(url):
    try:
        # 指定したエンドポイントのHTMLからtableに関する部分を取得
        table_data = pd.read_html(url)[0]
        print('[Success] Succeeded in acquiring HTML Table data from the specified endpoint.')
        return table_data
    except Exception as e:
        print('[Failure] Failed to get HTML Table data from the specified endpoint.')

def get_optimized_endpoint(table_data):
    try:
        # エンドポイントリストの初期化
        endpoint_list = []
        for service_type in service_type_list:
            # サービスタイプでフィルターをかけてテーブル作成
            service_data = table_data[table_data['Service Type'] == service_type]
            # table内のサクセスレートの最大値を取得
            max_success_rate = service_data['Success Rate (%)'].max()
            # table内のサクセスレートが最も高いデータのみでテーブル作成
            service_maxssuccessrate_data = service_data[service_data['Success Rate (%)'] == max_success_rate]
            # table内のレイテンシーの最小値を取得
            max_average_latency = service_maxssuccessrate_data['Average Latency (seconds)'].min()
            # table内でレイテンシーが最も良いデータのみでテーブル作成
            service_best_data = service_maxssuccessrate_data[service_maxssuccessrate_data['Average Latency (seconds)'] == max_average_latency]
            # 最適化エンドポイントを取得
            best_endpoint = service_best_data.iloc[0, 2]
            endpoint_list.append(best_endpoint)
        print('[Success] The current optimization endpoint is Swapcaser = %s, Leeter = %s, Reverser = %s' % (endpoint_list[0], endpoint_list[1], endpoint_list[2]))
        return endpoint_list
    except Exception as e:
        print('[Failure] Failed to get current optimization endpoint')
        print('[Reason] %s' % e)

def get_delete_key():
    try:
        delete_key_list = []
        items = table.scan()['Items']
        for item in items:
            key_data = item.pop('TeamName')
            delete_key_list.append(item)
        print('[Success] Scan of DynamoDB table was successful (table_name = %s)' % table_name)
        return delete_key_list
    except ClientError as e:
        print('[Failure] Scan of DynamoDB table failed (table_name = %s)' % table_name)
        print('[Reason] %s' % e)
    except Exception as e:
        print('[Failure] Scan of DynamoDB table failed (table_name = %s)' % table_name)
        print('[Reason] %s' % e)

def put_new_endpoint(endpoint_list, delete_key_list):
    try:
        for index in range(len(service_type_list)):
            item = {"Endpoint": endpoint_list[index], "ServiceType": service_type_list[index], "TeamName": team_name}
            table.put_item(Item=item)
            key_data = item.pop('TeamName')
            if item in delete_key_list:
                delete_key_list.remove(item)
        print('[Success] The record was successfully registered in DynamoDB (table_name = %s)' % table_name)
        delete_old_record(delete_key_list)
    except ClientError as e:
        print('[Failure] Failed to register record in DynamoDB (table_name = %s)' % table_name)
        print('[Reason] %s' % e)
    except Exception as e:
        print('[Failure] Failed to register record in DynamoDB (table_name = %s)' % table_name)
        print('[Reason] %s' % e)
        
def delete_old_record(delete_key_list):
    try:
        for delete_key in delete_key_list:
            table.delete_item(Key=delete_key)
        print('[Success] Successfully deleted old records in DynamoDB (table_name = %s)' % table_name)
    except ClientError as e:
        print('[Failure] Failed to delete old record in DynamoDB (table_name = %s)' % table_name)
        print('[Reason] %s' % e)
    except Exception as e:
        print('[Failure] Failed to delete old record in DynamoDB (table_name = %s)' % table_name)
        print('[Reason] %s' % e) 
