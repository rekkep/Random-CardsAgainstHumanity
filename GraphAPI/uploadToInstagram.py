from GraphAPI.getCreds import makeApiCall



'''
1. Creating IG User Media
    Images:
        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media
        ?image_url={image-url}
        &is_carousel_item={is-carousel-item}
        &caption={caption}
        &location_id={location-id}
        &user_tags={user-tags}
        &access_token={access-token}
    image_url: Required for images. Applies only to images.
                The path to the image. Must be on public server
    is_carousel_item:
    
    reponse:
        JSON-formattet object containing an IG Container ID.


2. Publishing IG User Media

        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media_publish
        ?creation_id={creation-id}
        &access_token={access-token}
    ig-user-id: ig-user-id
    creation_id: response from 'Creating IG User Media'
    access_token: access-token 
    
    response:
        id of the published media

'''




def createImageContainer(params:dict, image_url:str, is_carousel_item='false', caption:str='', location_id='', user_tags='', auto_upload:bool = False, api_call_debug:bool=False):
    """Creates the container-Id for the image, provided by the image_url. The container-ID is used to upload the image to instagram.
    
    ------
    ------

    Args:
    -----
        params (dict): 
            contains all necessary parametes for the api:
                ig_user_id, base_url and access_token.\tStored in your JSON-file and paresd by getCreds-method\n
        image_url (str): 
            Required for images. The path to the image. We will cURL the image using the passer URL so it must be on a public server.\n
        is_carousel_item (str, optional): 
            Set to 'true'. Indicates the image appears in a carousel. Defaults to 'false'.\n
        caption (str, optional): 
            A caption for the image. Can include hashtags (#) and usernames of Instagram users (@USERNAME). @Mentioned Instagram users receive a notification when the container is published. Maximum 2200 characters, 30 hashtags and 20 @ tags. 
            Defaults to ''.\n
        location_id (str, optional): 
            The ID of a Page associated with a location that you want to tag the image with. Use the Pages Search API to search for Pages whose names match a search string, then parse the results to identify any Pages that have been created for a physical location. Include the location field in your query and verify that the Page you want to use has location data. Attempting to create a container using a Page that has no location data will fail with coded exception INSTAGRAM_PLATFORM_API__INVALID_LOCATION_ID. Not supported on images or videos in carousels.. Defaults to ''.\n
        user_tags (str, optional): 
            An array of public usernames and x|y coordinates for any public Instagram users who you want to tag in the image. The array must be formatted in JSON and contain a username, x and y, property, such as [{username:'USERNAME',x:0.5,y:1.0}]. x and y values must be float numbers that originate from the top-left of the image, with a range of 0.0-1.0. Tagged users receive a notification when you publish the image container. Defaults to ''.\n
        auto_upload (bool, optional): 
            Creates the image container and upload the image directly to instagram. Defaults to False.\n
        api_call_debug (bool, optional): 
            Debug tool for API-calls. Prints all parametes and responses to the console. Defaults to False.\n

    Returns:
    --------
        id: Return the container-id of the image when auto_upload is set to False. If auto_upload is set to True. The image is published and the post id is returned.
        
    API-Call:
    ---------
        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
            ?image_url={image-url}\n
            &is_carousel_item={is-carousel-item}\n
            &caption={caption}\n
            &location_id={location-id}\n
            &user_tags={user-tags}\n
            &access_token={access-token}
    """    

    
    #creates the API-endpoint
    ig_user_id = params['ig_user_id']
    endpoint_url = f'{ig_user_id}/media'
    url = params['base_url'] + endpoint_url
    
    #creates the endpoint parameters
    endpoint_params = dict()
    endpoint_params['image_url'] = image_url
    endpoint_params['is_carousel_item'] = is_carousel_item
    endpoint_params['caption'] = caption
    #endpoint_params['location_id'] = location_id
    #endpoint_params['user_tags'] = user_tags
    endpoint_params['access_token'] = params['access_token']
    
    #checks for auto upload
    if auto_upload:
        #publish the image ans returns the post id
        return uploadMedia(params, makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)['json_response_data']['id'])
    else:
        #returns the container id
        return makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)['json_response_data']['id']
    
    
   
def createVideoContainer(params:dict, video_url:str, is_carousel_item='false', caption='', location_id='', thumb_offset='0', auto_upload:bool = False, api_call_debug:bool=False):
    """Creates the container-Id for the video, provided by the video_url. The container-ID is used to upload the video to instagram.

    -----
    -----
    
    Args:
    -----
        params (dict): 
            Contains all necessary parameters for the api:
                ig_user_id, base_url and access_token. Stored in the JSON-file and provided by the getCreds()-function.\n
        video_url (str): 
            Required for videos. Path to the video. We cURL the video using the passed-in URL, so it must be on a public server.\n
        is_carousel_item (str, optional): 
            Set to 'true'. Indicates the image appears in a carousel. Defaults to 'false'.\n
        caption (str, optional): 
            A caption for the image. Can include hashtags (#) and usernames of Instagram users (@USERNAME). @Mentioned Instagram users receive a notification when the container is published. Maximum 2200 characters, 30 hashtags and 20 @ tags. 
            Defaults to ''.\n
        location_id (str, optional): 
            The ID of a Page associated with a location that you want to tag the image with. Use the Pages Search API to search for Pages whose names match a search string, then parse the results to identify any Pages that have been created for a physical location. Include the location field in your query and verify that the Page you want to use has location data. Attempting to create a container using a Page that has no location data will fail with coded exception INSTAGRAM_PLATFORM_API__INVALID_LOCATION_ID. Not supported on images or videos in carousels. 
            Defaults to ''.\n
        thumb_offset (str, optional): 
            Location, in milliseconds, of the video frame to be used as the video's cover thumbnail image. 
            Defaults to '0'.\n
        auto_upload (bool, optional): 
            Creates the image container and upload the image directly to instagram. 
            Defaults to False.\n
        api_call_debug (bool, optional): 
            Debug tool for API-calls. Prints all parametes and responses to the console. 
            Defaults to False.\n

    Returns:
    --------
        id: Return the container-id of the image when auto_upload is set to False. If auto_upload is set to True. The image is published and the post id is returned.
    
    API-Call:
    ---------
        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
            ?media_type=VIDEO\n
            &video_url={video-url}\n
            &is_carousel_item={is-carousel-item}\n
            &caption={caption}\n
            &location_id={location-id}\n
            &thumb_offset={thumb-offset}\n
            &access_token={access-token}
    """        
     
    #creates the API-endpoint
    ig_user_id = params['ig_user_id']
    endpoint_url = f'{ig_user_id}/media'
    url = params['base_url'] + endpoint_url
    
    #creates the endpoint parameters
    endpoint_params = dict()
    endpoint_params['media_type'] = 'VIDEO'
    endpoint_params['video_url'] = video_url
    endpoint_params['is_carousel_item'] = is_carousel_item
    endpoint_params['caption'] = caption
    #endpoint_params['location_id'] = location_id
    endpoint_params['thumb_offset'] = thumb_offset
    endpoint_params['access_token'] = params['access_token']
    
    #checks for auto upload
    if auto_upload:
        #publisch the video ans returns the post id
        return uploadMedia(params, makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)['json_response_data']['id'])
    else:
        #returns the container id
        return makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)['json_response_data']['id']



def createCarouselsContainer(params:dict, children:list, caption:str='', location_id='', auto_upload:bool = False, api_call_debug:bool=False):
    """Creates container id for the carousel, provided by the children. The container-ID is used to publish the media to instagram.

    ----
    ----
    
    Args:
    -----
        params (dict): 
            Contains all necessary parameters for the api:\n
                ig_user_id, base_url and access_token. Stored in your JSON-file and parsed by the getCreds()-function\n
        children (list): 
            Required for carousels. An array of up to 10 container IDs of each image and video that should appear in the published carousel. Carousels can have up to 10 total images, videos or a mix of the two.\n
        caption (str, optional): 
            A caption for the image, video, or carousel. Can include hashtags (example: #crazywildebeest) and usernames of Instagram users (example: @natgeo). @Mentioned Instagram users receive a notification when the container is published. Maximum 2200 characters, 30 hashtags, and 20 @ tags. \
            Defaults to ''.\n
        location_id (str, optional): 
            The ID of a Page associated with a location that you want to tag the image or video with. Use the Pages Search API to search for Pages whose names match a search string, then parse the results to identify any Pages that have been created for a physical location. Include the location field in your query and verify that the Page you want to use has location data. Attempting to create a container using a Page that has no location data will fail with coded exception INSTAGRAM_PLATFORM_API__INVALID_LOCATION_ID. \
            Defaults to ''.\n
        auto_upload (bool, optional): 
            Creates the carousel container and upload the carousel directla to instagram. \
            Defaults to False.\n
        api_call_debug (bool, optional): 
            Debug tool for API-calls. Prints all parameters and responses to the console. \
            Defaults to False.\n

    Returns:
    --------
        ID: Returns the container-ID of the carousels when auto_upload is set to False. If auto_upload is set to True, the carousel is published and the post-id is returned.
    
    API-Call:
    ---------
        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
            ?media_type=CAROUSEL\n
            &caption={caption}\n
            &location_id={location-id}\n
            &children={children}\n
            &access_token={access-token}
    
    
    """    
    

    #creates the API-endpoint
    ig_user_id = params['ig_user_id']
    endpoint_url = f'{ig_user_id}/media'
    url = params['base_url'] + endpoint_url
    
    #creates the endpoint parameters
    endpoint_params = dict()
    endpoint_params['media_type'] = 'CAROUSEL'
    
    child = ''
    for n, Id in enumerate(children):
        child += Id
        if n < len(children) - 1:
            child += ','
    
    endpoint_params['children'] = child
    endpoint_params['caption'] = caption
    #endpoint_params['location_id'] = location_id
    endpoint_params['access_token'] = params['access_token']
    
    #checks for auto upload
    if auto_upload:
        #publish the image and returns the post id
        return uploadMedia(params, makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)['json_response_data']['id'])
    else:
        #returns the container id
        return makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)#['json_response_data']['id']



def createCarouselsChildren(params:dict, media_urls:list, media_type:list, caption:str='', location_id='', auto_upload:bool = False, api_call_debug:bool=False):
    """Creates children list with container-IDs for a carousel post.
    
    ----
    ----
    
    Args:
    -----
        params (dict): 
            Contains all necessary parameters for the api:\n
                ig_user_id, base_url and access_token. Stored in your JSON-file and parsed by the getCreds()-function.
        media_urls (list): 
            All paths to the published media. We will cURL the media using the passed in URLs so it must be on a public server.\n
        media_type (list): 
            The type of media to be published. Must be 'IMAGE' or 'VIDEO'!\n
        caption (str, optional): 
            A caption for the image. Can include hashtags (#) and usernames of Instagram users (@USERNAME). @Mentioned Instagram users receive a notification when the container is published. Maximum 2200 characters, 30 hashtags and 20 @ tags. 
            Defaults to ''.\n
        location_id (str, optional): 
            The ID of a Page associated with a location that you want to tag the image with. Use the Pages Search API to search for Pages whose names match a search string, then parse the results to identify any Pages that have been created for a physical location. Include the location field in your query and verify that the Page you want to use has location data. Attempting to create a container using a Page that has no location data will fail with coded exception INSTAGRAM_PLATFORM_API__INVALID_LOCATION_ID. Not supported on images or videos in carousels. 
            Defaults to ''.\n
        auto_upload (bool, optional): 
            Creates the image container and upload the image directly to instagram. Defaults to False.\n
        api_call_debug (bool, optional): 
            Debug tool for API-calls. Prints all parametes and responses to the console. Defaults to False.\n
    
    Returns:
    --------
        ID: Returns the container-ID of the carousels when auto_upload is set to False. If auto_upload is set to True, the carousel is published and the post-id is returned.
    
    API-Call:
    ---------
    ---------
        Image:
        ------
            POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
                ?image_url={image-url}\n
                &is_carousel_item={is-carousel-item}\n
                &caption={caption}\n
                &location_id={location-id}\n
                &user_tags={user-tags}\n
                &access_token={access-token}
            
        Video:
        ------
            POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
                ?media_type=VIDEO\n
                &video_url={video-url}\n
                &is_carousel_item={is-carousel-item}\n
                &caption={caption}\n
                &location_id={location-id}\n
                &thumb_offset={thumb-offset}\n
                &access_token={access-token}
        
        Carousel:
        ---------
            POST https://graph.facebook.com/{api-version}/{ig-user-id}/media\n
                ?media_type=CAROUSEL\n
                &caption={caption}\n
                &location_id={location-id}\n
                &children={children}\n
                &access_token={access-token}
        
    """    
    
    children = list()
    
    for n, media_type in enumerate(media_type):
        if media_type == 'IMAGE':
            container_id = createImageContainer(params, media_urls[n], 'true')
        elif media_type == 'VIDEO':
            container_id = createVideoContainer(params, media_urls[n], 'true')
        else:
            print(f"ERROR: {media_type} is no valid media_type. Media_type must be 'IMAGE' or 'VIDEO', not {media_type}!\nEntry is skipped.")
            continue
        children.append(container_id)

    return createCarouselsContainer(params, children, caption, location_id, auto_upload, api_call_debug)



def uploadMedia(params:dict, creation_id, api_call_debug:bool=False):
    """Upload and publish the media provided by the creation_id.
    
    ----
    ----

    Args:
    -----
        params (dict): 
        Contains all neccessary parameters for the api:\n
            ig_user_id, base_url and access_token. Stored in your JSON-file and parsed by getCreds()-function.\n
        creation_id (_type_): 
            The ID of the IG Container to be published, generated by createImageContainer(), createVideoContainer() or createCarouselsContainer()-function.\n
        api_call_debug (bool, optional): 
            Debug tool for API-calls. Prints all parametes and responses to the console. \n
            Defaults to False.

    Returns:
    --------
        _type_: Media is published and the post-id is returned.
        
    API-Call:
    ---------
        POST https://graph.facebook.com/{api-version}/{ig-user-id}/media_publish\n
            ?creation_id={creation-id}\n
            &access_token={access-token}
    """    

    #creates the API-endpoint
    ig_user_id = params['ig_user_id']
    endpoint_url = f'{ig_user_id}/media_publish'
    url = params['base_url'] + endpoint_url
    
    #creatse endpoint parameters
    endpoint_params = dict()
    endpoint_params['creation_id'] = creation_id
    endpoint_params['access_token'] = params['access_token']
    
    #publishe the media and return the post id
    return makeApiCall(url, endpoint_params, method='POST', debug=api_call_debug)




'''
TODO:

createImageContainer:
    caption: limitation
        max chars
        max #
        max @
        no caption if carousel
    location_id
    user_tags

createVideoContainer:
    caption: limitation
        max chars
        max #
        max @
        no caption if carousel
    location_id
    user_tags
    
createCarouselsContainer:
    caption: limitation
        max chars
        max #
        max @
        no caption if carousel
    location_id
    open for container insted of URLs
    limitation of 10 urls or containers
    

'''