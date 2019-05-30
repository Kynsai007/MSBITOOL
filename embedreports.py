import requests
def get_access_token():
    username = 'jaishree.v@datasemantics.in'
    password = 'Varadharaju5'
    client_id = 'c303a621-6f78-42ac-a368-a565f7bd40e1'
    data = {
        'grant_type': 'password',
        'scope': 'openid',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'client_id': client_id,
        'username': username,
        'password': password
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
    return response.json().get('access_token')

def get_embed_token(access_token,group_id,report_id):
    dest = 'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports/' + report_id + '/GenerateToken'
    headers = {'Authorization': 'Bearer ' + access_token}
    settings = { 'accessLevel': 'view' }
    response = requests.post(dest, data=settings, headers=headers)
    token = response.json().get('token')
    return token
def get_embeddashboard_token(access_token,group_id,dashboard_id):
    dest = 'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/dashboards/' + dashboard_id + '/GenerateToken'
    headers = {'Authorization': 'Bearer ' + access_token}
    settings = { 'accessLevel': 'view' }
    response = requests.post(dest, data=settings, headers=headers)
    token = response.json().get('token')
    return token

def get_datasetkey(access_token,group_id,datasetid):
    dest = 'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports/GenerateToken'
    headers = {'Authorization': 'Bearer ' + access_token}
    settings = { 'accessLevel': 'create','datasetId':datasetid,'allowSaveAs': 'true'}
    response = requests.post(dest, data=settings, headers=headers)
    token = response.json().get('token')
    return token   
    

    
