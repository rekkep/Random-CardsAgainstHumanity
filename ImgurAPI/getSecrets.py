from json import load


def getSecrets(path):
    
    
    secrets = dict()
    
    with open(path, 'r') as f:
        data = load(f)
        
        secrets['client_id'] = data['client_id']
        secrets['client_secret'] = data['client_secret']
        secrets['access_token'] = data['access_token']
        secrets['refresh_token'] = data['refresh_token']
    
    return secrets