import requests, json


file_path = str

def getCreds(script_path:file_path, key_path:file_path='/GraphAPI/GraphSecrets/GraphSecrets.json'):
    """Returns important informations for all API-Calls.

    Args:
    -----
        script_path (file_path): Path of the main script.
        key_path (file_path, optional): Path to the file, that stores API-Key. File must be in the same folder as the main-file! Defaults to '/API calls/stored infos.json'.

    Returns:
    --------
        _type_: Returns client_id, client_secret, access_token, ig_user_id, graph_domain, graph_version and base_url.
    """    
    
    file = str(script_path) + key_path
    
    params = dict()
    
    #store the parameters from the file to an dict
    with open(file, 'r') as f:
        data = json.load(f)
        
        params['client_id'] = data['client_id']
        params['client_secret'] = data['client_secret']
        params['access_token'] = data['access_token']
        params['ig_user_id'] = data['ig_user_id']
    

    params['graph_domain'] = 'https://graph.facebook.com/'
    params['graph_version'] = 'v13.0'
    params['base_url'] = params['graph_domain'] + params['graph_version'] + '/'
    
    return params
    
    
def makeApiCall(url, endpointParams, debug = False, method='GET'):
    """Makes an API-Call with the given Url and parameters.

    Args:
    -----
        url (url:str): The called API-Url.
        endpointParams (dict): Necessary endpointparameters for the API-Call.
        debug (bool, optional): Debug-tool for the API-Call. Print all parameters and the response from the API-call to the console. Defaults to False.
        method (str, optional): API-Call methode. Defaults to 'GET'.

    Returns:
    --------
        _type_: Returns the response of the API-Call.
    """    
    
    #API-Call with the given informations
    response_data = requests.request(method=method, url=url, params=endpointParams)
    
    #stores all given parameters and the response to an dict
    response = dict()
    response['method'] = method
    response['url'] = url
    response['json_endpoint_params'] = endpointParams
    response['json_response_data'] = response_data.json()
    
    #debug tool
    #prints all given parameters and the response to the console
    if debug:
        for entry in response:
            if 'json' in entry:
                print(f'{entry}:\n{json.dumps(response[entry], indent=4)}')
            else:
                print(f'{entry}:\n{response[entry]}')
    
    return response
        