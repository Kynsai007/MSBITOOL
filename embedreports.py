import requests
def get_access_token():
    username = 'sandhya.b@datasemantics.in'
    password = 'S@n#ds17'
    client_id = '153d8262-d79d-47f8-91da-6bae14ad617a'
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

def get_datasetkey(access_token,group_id,dataset_id):
    dest = 'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports/GenerateToken'
    headers = {'Authorization': 'Bearer ' + access_token}
    settings = { 'accessLevel': 'create', 'datasetId' : dataset_id, 'allowSaveAs': 'true'}
    response = requests.post(dest, data=settings, headers=headers)
    token = response.json().get('token')
    return token   
    

    
