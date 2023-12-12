import datetime
import configparser
from base64 import b64decode
import webbrowser
import openai
from openai.error import InvalidRequestError #this helps to prevent error when uploading files. Also gives me description of the error so it can be fixed.

def generate_image(prompt, num_image=1, size='512x512', output_format='url'):
    """
    params:
       prompt (str):
       num_image (int):
       size (str):
       output_format (str):
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=num_image,
            size=size,
            response_format=output_format
        )
        if response is not None:  # This checks if response is not None
            images = []
            if output_format == 'url':
                for image in response['data']:
                    images.append(image.url)
            elif output_format == 'b64_json':
                for image in response['data']:
                    images.append(image.b64_json)
            return {'created': datetime.datetime.fromtimestamp(response['created']),'images': images}
        else:
            # Handles the case when response is None
            print("Image creation failed.")
    except InvalidRequestError as e:
        print(e)


config = configparser.ConfigParser()
config.read('credential.ini')
API_KEY = config['openai']['APIKEY']
#connecting API here. Refresh and add KEY every few days to optimize quality.
openai.api_key = API_KEY 

SIZES = ('1024x1024', '512x512', '256x256', '528x720')
#for smaller size '1024x1024', '512x512', '256x256', '528x720' for 5x7 inch images place in '1500x2100', '1200x1680', '900x1260', '360x504'

response = generate_image('write or insert prompt here', num_image=2, size=SIZES[1], output_format= 'b64_json')
prefix= 'ai_build'
for indx, image in enumerate(response['images']):
    with open(f'{prefix}_{indx}.png', 'wb') as f:
        f.write(b64decode(image))
