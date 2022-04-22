from getCreds import getCreds, makeApiCall
import json
from os import path
from sys import argv




def exchangeToken(params:dict, fbExchangeToken:str):    
    """get new valid access_token\n
    valid for 60 days

    Args:
    ----
        params (dict): list with response params\n
        fbExchangeToken (str:token): expiring active token

    Returns:
    -------
        dict: {'access_token': ACCESS_TOKEN, 'token_type': 'bearer'}
        
    ----
    ----

    API-call:
    --------
        url -i -X GET "https://graph.facebook.com/oauth/access_token?\n
            grant_type=fb_exchange_token&\n
            client_id={APP-ID}&\n
            client_secret={APP-SECRET}&\n
            fb_exchange_token={SHORT-LIVED-USER-ACCESS-TOKEN}"
    """    
    
    endpoint_url = 'oauth/access_token'
    
    endpoint_params = dict()
    endpoint_params['grant_type'] = 'fb_exchange_token'
    endpoint_params['client_id'] = params['client_id']
    endpoint_params['client_secret'] = params['client_secret']
    
    endpoint_params['fb_exchange_token'] = fbExchangeToken
    
    url = params['base_url'] + endpoint_url
    
    return makeApiCall(url, endpoint_params, True)['json_response_data']['access_token']



def updateStoredToken(showToken:bool=False):
    """Updates the stored access_token.

    Args:
    -----
        showToken (bool, optional): Prints the new access token to the console. Defaults to False.
    """    
    
    file = f'{path.dirname(argv[0])}/GraphSecrets/GraphSecrets.json'
    
    
    with open(file, 'r') as in_file:
        data = json.load(in_file)
    
    data['access_token'] = exchangeToken(getCreds(), data['access_token'])

    
    with open(file, 'w') as out_file:
        json.dump(data, out_file, indent=4)
        
    if showToken:
        print(f'The new access_token is:\n{data["access_token"]}')


