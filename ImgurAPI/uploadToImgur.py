from imgurpython import ImgurClient
from json import dumps, load

def getSecrets(script_path):
    
    imgur_secrets = script_path + '/ImgurAPI/ImgurSecrets/ImgurSecrets.json'
    
    secrets = dict()

    with open(imgur_secrets, 'r') as f:
        data = load(f)
        
        
        secrets['client_id'] = data['client_id']
        secrets['client_secret'] = data['client_secret']
        secrets['access_token'] = data['access_token']
        secrets['refresh_token'] = data['refresh_token']
    
    return secrets


def uploadImage(script_path, image_path, album=None, name:str='', title:str='', description:str='', console_log:bool=False, anon:bool=False):
    
    client = getClient(script_path)
    
    config = {
        'album': album,
        'name': name,
        'title': title,
        'description': description
    }
    
    
    if console_log:
        print('Uploading image to Imgur... ')
        image = client.upload_from_path(image_path, config=config, anon=anon)
        print('Done!')
        print(f'Image informations:\n{dumps(image, indent=4)}')
    else:
        image = client.upload_from_path(image_path, config=config, anon=anon)
        
    return image



def getClient(script_path):
    #path = 'TODO: Path to imgur secrets'
    
    secrets = getSecrets(script_path)
    return ImgurClient(secrets['client_id'], secrets['client_secret'], secrets['access_token'], secrets['refresh_token'])