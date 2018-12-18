#!/usr/bin/env python3


import base64
import googleapiclient.discovery
from os import path


def get_project_dir():
    path_array = path.dirname(path.realpath(__file__)).split('/')
    proj_root = "/".join(path_array[:len(path_array) - 1])
    return proj_root

speech_file = path.join(path.realpath(get_project_dir()),
                       "resources",
                       "harvard.raw")

with open(speech_file, 'rb') as speech:
    # Base64 encode the binary audio file for inclusion in the JSON
    # request.
    speech_content = base64.b64encode(speech.read())


# Construct the request
service = googleapiclient.discovery.build('speech', 'v1')

service_request = service.speech().recognize(
        body={
            "config": {
                "encoding": "LINEAR16",  # raw 16-bit signed LE samples
                "sampleRateHertz": 16000,  # 16 khz
                "languageCode": "en-US",  # a BCP-47 language tag
            },
            "audio": {
                "content": speech_content
            }
        })

response = service_request.execute()
recognized_text = 'Transcribed Text: \n'
for i in range(len(response['results'])):
    recognized_text += response['results'][i]['alternatives'][0]['transcript']

print(recognized_text)

