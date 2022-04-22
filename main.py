from random import randrange
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from ImgurAPI import uploadToImgur
from GraphAPI import uploadToInstagram, getCreds
from os import remove, path
from sys import argv
from datetime import datetime



file_path = str


def choose_card(prompt_cards_file: file_path, prompt_symbol: str, response_cards_file: file_path, spacer: str, seperator: str):
    '''
    Generates a random cards against humanity combination
    
       
    Return
    ------
    the random CAD-combination : str
        string of the random CAD-combination
        
    prompt card number : int
        number of the promt card
        
    prompt card set : str
        set of the prompt count
        
    response card number/s : list
        list of all numbers of the responses
        
    response card set/s : list
        list of all sets of the responses
    
    
    Atributes - inputs
    ------------------
    prompt_card_file : path
        file path of the prompt card-file (black cards)
        
    prompt_symbol : str
        the symbol, that indicates the place for the response card/s
        
    response_cards_file : path
        file path of the response cards-file (white cards)
        
    spacer : str
        symbol/string that indicates the end of a card
        
    seperator : str
        symbol/string that seperates card from card-set    
    '''

    with open(prompt_cards_file, 'r', encoding='utf-8') as prompt_file:
        prompt_cards = prompt_file.read().split(spacer)  # -> list(prompt&set)
    prompt_number = randrange(len(prompt_cards)-1)
    prompt_question = prompt_cards[prompt_number].find('?\n<response>')
    prompt, prompt_set = prompt_cards[prompt_number].split(seperator)
    prompt_count = prompt.count(prompt_symbol)

    with open(response_cards_file, 'r', encoding='utf-8') as response_file:
        response_cards = response_file.read().split(spacer)  # -> list(response&set)
    response_numbers, responses, response_sets = [], [], []
    for n in range(prompt_count):
        response_numbers.append(str(randrange(len(response_cards)-1)))
        response_temp, response_set_temp = response_cards[int(
            response_numbers[n])].split(seperator)
        if prompt_question == -1:
            response_temp = response_temp.replace('.', '')
        responses.append(response_temp)
        response_sets.append(response_set_temp)
    for response in responses:
        prompt = prompt.replace(prompt_symbol, f'>{response}<', 1)

    if len(response_sets) > 1:
        response_numbers = '; no.'.join(response_numbers)
        response_sets = '; '.join(response_sets)
        caption = f'prompt: #{prompt_number}\tresponse: #{response_numbers}\nprompt-set: {prompt_set}\tresponse-set: {response_sets}\n%23CradsAgainstHumanity'
        print(caption)
    else:
        response_numbers = response_numbers[0]
        response_sets = response_sets[0]
    caption = f'prompt: #{prompt_number}\tresponse: #{response_numbers}\nprompt-set: {prompt_set}\tresponse-set: {response_sets}\n%23CradsAgainstHumanity'

    return prompt, prompt_number, prompt_set, response_numbers, response_sets, caption


def create_image(prompt: str, base_path:file_path, img_width: int = 1080, img_height: int = 1080, img_show:bool=False, img_save:bool=False, print_combination:bool=False, combination:str=''):
    '''
    Creates an black Image with promt on it
    
    Return
    ------
    
    Atributes - inputs
    ------------------
    
    '''
    text_width = 40

    font_file = [f'{base_path}/font/comfortaa/Comfortaa-Light.ttf',
                 f'{base_path}/font/comfortaa/Comfortaa-Bold.ttf',
                 f'{base_path}/font/comfortaa/Comfortaa-Light.ttf']
    prompt_font_file, response_font_file, combination_font_file = font_file
    font_size = 40

    img_size = (img_width, img_height)

    text = wrap(prompt, width=text_width)
    prompt_font = ImageFont.truetype(prompt_font_file, font_size)
    response_font = ImageFont.truetype(response_font_file, font_size)
    combination_font = ImageFont.truetype(combination_font_file, int(font_size/2))
    font_used = prompt_font

    img = Image.new('RGB', img_size)
    draw = ImageDraw.Draw(img)

    #current_height = start_height = 300
    line_space = 70

    line_count = len(text)
    txt_width, txt_height = draw.textsize(text[0], font_used)
    total_height = line_count * txt_height
    start_height = img_height/2 - total_height
    current_height = start_height

    # draw.line((img_width/2, 0, img_width/2, start_height))
    # draw.line((0, img_height/2, img_width, img_height/2))

    for line in text:
        line_width, line_height = draw.textsize(line, font_used)
        offset_x, offset_y = font_used.getoffset(line)#.encode('utf-8'))
        line_width += offset_x
        current_width = img_width/2 - line_width/2
        
        for word in line.split(' '):
            #print(word)
            if '>' in word:
                font_used = response_font
                word = word.replace('>', '')
            if '<' in word:
                word = word.replace('<', '')
                draw.text((current_width, current_height),
                          word, font=font_used)
                font_used = prompt_font
            else:
                draw.text((current_width, current_height),
                          word, font=font_used)
            word_width, word_height = draw.textsize(f'{word} ', font_used)
            offset_x, offset_y = font_used.getoffset(f'{word} ')
            word_width += offset_x
            
            
            current_width += word_width
            
        
        # draw.rectangle((current_width, current_height,
        #             20+current_width, 20+current_height))
        #draw.text((img_width/2, current_height), line, anchor='mm', font=base_font)
        current_height += line_height + line_space
    
    if print_combination:      
        draw.text((10, 1000), combination, font=combination_font)        
    # offset_x, offset_y = base_font.getoffset(text)


    # width_text += offset_x
    # height_text += offset_y

    # top_left_x = width_image / 2 - width_text / 2
    # top_left_y = height_image / 2 - height_text / 2
    # xy = top_left_x, top_left_y

    # draw.text(xy, text, font=font, fill=color)

    if img_show:
        img.show()
    if img_save:
        save_path = f'{base_path}/images/image-{str(datetime.now()).replace(":", "-")}.jpg'
        img.save(save_path)
        return img, save_path
    
    return img


def imgurUpload(script_path, img, album=None, name:str='', title:str='', description:str='', console_log:bool=False, anon:bool=False, show_progress:bool = True):

    if show_progress:
        print('Uploading to Imgur... ')
    image = uploadToImgur.uploadImage(script_path, img, album, name, title, description, console_log, anon)
    if show_progress:
        print(f'Upload to imgur finished. The url to your image is {image["link"]}')
    return image


def instaUpload(script_path, media_type:str, media_url=None, caption:str='', auto_upload:bool=True, api_debug:bool=False, show_progress:bool=True, media_urls:list=None, media_types:list=None, children_list:list=None):
    """Uploads Media to instagram.

    Args:
    -----
        script_path (_type_): Path of the main folder.
        media_url (_type_): Url to the media. Must be on a public server!
        media_type (str, optional): Type of media. Must be one of the following strings: 'IMAGE' | 'VIDEO' | 'CAROUSEL_CHILDREN' | 'CAROUSEL'.
        caption (str, optional): Caption of the upload. Defaults to ''.
        auto_upload (bool, optional): Uploads the media automatically to instagram. Defaults to True.
        api_debug (bool, optional): Debug tool for the API. Prints all information to the console. Defaults to False.
        show_progress (bool, optional): Prints the progress of the upload to the console. Defaults to True.
        media_urls (list, optional): If carousel_children is selected, a list of the urls to the media must be provided. Max 10. Defaults to None.
        media_types (list, optional): If carousel_children is selected, a list of the type of media must be provided. Max 10. Defaults to None.
        children_list (list, optional): If carousel is selected, a list with the media IDs must be provided. Max 10. Defaults to None.
        
    Return:
    -------
        response (_type_): Returns the response from the API
    """    
    params = getCreds.getCreds(script_path)
    
    
    if media_type == 'IMAGE':
        if auto_upload and show_progress:
            print('Uploading image to instagram... ')
        elif not auto_upload and show_progress:
            print('Creating image container... ')
        response = uploadToInstagram.createImageContainer(params, media_url, caption=caption, auto_upload=auto_upload, api_call_debug=api_debug)
        if auto_upload and show_progress:
            print('Done!')
        elif not auto_upload and show_progress:
            print('Done!')
        
        return response
        
        
    elif media_type == 'VIDEO':
        if auto_upload and show_progress:
            print('Uploading video to instagram... ')
        elif not auto_upload and show_progress:
            print('Creating video container... ')
        response = uploadToInstagram.createVideoContainer(params, media_url, caption=caption, auto_upload=auto_upload, api_call_debug=api_debug)
        if auto_upload and show_progress:
            print('Done!')
        elif not auto_upload and show_progress:
            print('Done!')
        
        return response
        
        
    elif media_type == 'CAROUSEL_CHILDREN':
        if auto_upload and show_progress:
            print('Uploading carousel to instagram... ')
        elif not auto_upload and show_progress:
            print('Creating carousel container... ')
        response = uploadToInstagram.createCarouselsChildren(params, media_urls, media_types, caption, auto_upload=auto_upload, api_call_debug=api_debug)
        if auto_upload and show_progress:
            print('Done!')
        elif not auto_upload and show_progress:
            print('Done!')
        
        return response
        
        
    elif media_type == 'CAROUSEL':
        if auto_upload and show_progress:
            print('Uploading carousel to instagram... ')
        elif not auto_upload and show_progress:
            print('Creating carousel container... ')
        response = uploadToInstagram.createCarouselsContainer(params, children_list, caption, auto_upload=auto_upload, api_call_debug=api_debug)
        if auto_upload and show_progress:
            print('Done!')
        elif not auto_upload and show_progress:
            print('Done!')

        return response


def createPost(number_of_induvidual_posts:int=1, save_image:bool=False, combination_caption:bool=True, custom_caption:str='', is_carousel:bool=False, number_of_carousel:int=0, api_debug:bool=False):
    
    
    default_path = path.dirname(argv[0])
    
    prompt_file = default_path + '/card/Prompt Cards.txt'
    response_file = default_path + '/card/Response Cards.txt'
    
    
    if is_carousel and number_of_carousel > 10:
        print(f'Max number of carousel madia is exceeded. Maimum is 10 your input is {number_of_carousel}!')
        return
    
    
    if is_carousel:
        links, media_type, temp_caption = list(), list(), list()
        
        for _ in range(number_of_induvidual_posts):
            for _ in range(number_of_carousel):
                print('Choosing card combiation... ')
                card = choose_card(prompt_file, '<response>',
                                    response_file, '<end>\n', '<set>')
                prompt = card[0]
                combination = f'p{card[1]}|r{card[3]}'
                print(f'Card-combination is {combination}')
                print('Creating image... ')
                img = create_image(prompt, default_path, img_save=True, combination=combination)
                print('Uploading... ')
                imgur_image = imgurUpload(default_path, img[1])
                if not save_image:
                    remove(img[1])
                links.append(imgur_image['link'])
                media_type.append('IMAGE')
                
                temp_caption.append(f'\nprompt: no.{card[1]} respone: no.{card[3]}')
                if combination_caption:
                    caption = '\n'.join(temp_caption)
                    
                else:
                    caption = custom_caption
                    
                caption += '\n#CardsAgainstHumanity\n#GraphAPI\n#Python'

            
            instaImage = instaUpload(default_path, 'CAROUSEL_CHILDREN', caption=caption, auto_upload=True, media_urls=links, media_types=media_type, api_debug=api_debug)
            
    elif not is_carousel:
        for _ in range(number_of_induvidual_posts):
            print('Choosing card combiation... ')
            card = choose_card(prompt_file, '<response>',
                                response_file, '<end>\n', '<set>')
            prompt = card[0]
            combination = f'p{card[1]}|r{card[3]}'
            print(f'Card-combination is {combination}')
            print('Creating image... ')
            img = create_image(prompt, default_path, img_save=True, combination=combination)
            print('Uploading... ')
            imgur_image = imgurUpload(default_path, img[1])
            if not save_image:
                remove(img[1])
            if combination_caption:
                caption = f'\nprompt: no.{card[1]} respone: no.{card[3]}\n#CardsAgainstHumanity\n#GraphAPI\n#Python'
            elif not combination_caption:
                caption = custom_caption

            instaImage = instaUpload(default_path, 'IMAGE', imgur_image['link'], caption=caption, api_debug=api_debug)
    
    return instaImage

    


if __name__ == '__main__':
    
    default_path = path.dirname(argv[0])
    
    prompt_file = default_path + '/card/Prompt Cards.txt'
    response_file = default_path + '/card/Response Cards.txt'
    for _ in range(20):
        print('Choosing card combiation... ')
        card = choose_card(prompt_file, '<response>',
                            response_file, '<end>\n', '<set>')
        prompt = card[0]
        combination = f'p{card[1]}|r{card[3]}'
        print(f'Card-combination is {combination}')
        print('Creating image... ')
        img = create_image(prompt, default_path, img_save=True, combination=combination)
        img[0].show()
    #post = createPost(is_carousel=True, number_of_carousel=10)


'''
TODO
    -change prompt symbol and other seperators
    -upload to public (??imgur??)
    -upload to instagram
    -clean up code
        -docstring of function
        -more coments
        -image class #OOP
    -upload at a spezific time
    -more option for create_image
        -change background
        -change font
    -add combination #
        -black card no. + white card no.
        -save all combinations
            -prevent duplicates??
    -add card sets
        -as description of post
    -add watermark?
    -credis
        -font
        -cad reddit
            -authors of the list
    -test on raspberry pi
    -user interface
        -GUI or terminal based
    
    -file to generate txt files from excel list
        -type of file
            -txt or json
    -reuse code as an random motivation/poem generator
    -universal path
'''
