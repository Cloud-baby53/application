import pandas as pd
import time
import requests

team_name = '19Fujii'
url = 'http://original20010207.s3-website.us-east-2.amazonaws.com/'

def get_table_html():
    try:
        table_data = pd.read_html(url)[0]
        return table_data
    except Exception as e:
        print('[Failure] Failed to get HTML Table data from the specified endpoint.')

def get_myservice_endpoint(table_data):
    endpoint_data_table = table_data[table_data['Team Name'] == team_name]
    for endpoint in endpoint_data_table.itertuples():
        response = requests.post(endpoint[3], headers={'Content-Type':'application/json'}, json={"Message":"TestMessage"}, timeout=10)
        print('=============%s=======================' % endpoint[2])
        print('status_code = %s' % response.status_code)
        try:
            print('response_data = %s' % response.json())
        except:
            pass
        print('response_time = %s' % response.elapsed.total_seconds())

if __name__ == '__main__':
    while True:
        table_data = get_table_html()
        get_myservice_endpoint(table_data)
        time.sleep(15)
        