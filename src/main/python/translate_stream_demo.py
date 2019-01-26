#!/usr/bin/env python3
import argparse
import logging
import os
import re
import sys

import pyaudio
from google.api_core.exceptions import OutOfRange

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Audio recording parameters
from stream.microphone import MicrophoneStream
from utils import credentials
from services.translation import DeepLTranslationService


from dotenv import load_dotenv
load_dotenv()


RATE = 16000
# CHUNK = int(RATE / 10)  # 100ms
CHUNK = int(RATE / 12)


def listen_print_loop(responses, callback=print, debug=False, **kwargs):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            if debug:
                print(" * " + transcript)
            else:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()
                num_chars_printed = len(transcript)

        else:
            callback(transcript, **kwargs)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(stop streaming|exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def list_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = {}
    for i in range(0, num_devices):
        device = p.get_device_info_by_host_api_device_index(0, i)
        if (device.get('maxInputChannels')) > 0:
            devices[i] = device.get('name')
    return devices


def get_available_languages(answers):
    return [
               {
                   'key': 'en-US',
                   'name': 'English (United States)  ',
                   'value': 'en-US'
               },
               {
                   'key': 'en-GB',
                   'name': 'English (Great Britain)  ',
                   'value': 'en-GB'
               },
               {
                   'key': 'fr-FR',
                   'name': 'French (France)  ',
                   'value': 'fr-FR'
               },
               {
                   'key': 'pt-BR',
                   'name': 'Portuguese (Brazil)  ',
                   'value': 'pt-BR'
               },
               {
                   'key': 'pt-PT',
                   'name': 'Portuguese (Portugal)  ',
                   'value': 'pt-PT'
               },
               {
                   'key': 'es-ES',
                   'name': 'Spanish (Spain)  ',
                   'value': 'es-ES'
               },
               {
                   'key': 'de-DE',
                   'name': 'German  ',
                   'value': 'de-DE'
               },
               {
                   'key': 'nl-NL',
                   'name': 'Nederlands  ',
                   'value': 'nl-NL'
               }
           ]


def get_device_options(answers):
    return [f"{str(k)} - {v}" for k, v in list_devices().items()]


def read_options():
    from PyInquirer import prompt, style_from_dict, Token

    custom_style = style_from_dict({
        Token.Separator: '#6C6C6C',
        Token.QuestionMark: '#FF9D00 bold',
        # Token.Selected: '',  # default
        Token.Selected: '#5F819D',
        Token.Pointer: '#FF9D00 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#5F819D bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'list',
            'name': 'input-language',
            'message': 'Which language are you going to speak?',
            'choices': get_available_languages,
            'default': 0
        },
        {
            'type': 'list',
            'name': 'output-language',
            'message': 'Translate to which language?',
            'choices': get_available_languages,
            'default': 3
        },
        {
            'type': 'rawlist',
            'name': 'device',
            'message': 'Which device do you want to use?',
            'choices': get_device_options,
            'default': 0
        }

    ]
    answers = prompt(questions, style = custom_style)
    device_idx = int(answers['device'].split()[0])
    input_language = answers['input-language'].split()[0]
    output_language = answers['output-language'].split()[0]
    return input_language, output_language, device_idx


def create_configuration(input_language):
    config = create_recognition_configuration(input_language)
    return speech.types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)


def create_recognition_configuration(input_lang):
    return types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=input_lang,
            profanity_filter=True,
            # Enable automatic punctuation
            enable_automatic_punctuation=True)


def main(deepl_auth_key):

    input_lang, output_lang, device_index = read_options()
    translator = DeepLTranslationService(input_lang, output_lang, deepl_auth_key)

    def print_translation(text, **kwargs):
        response = translator.handle(text)
        translation = response['translations'][0]
        if 'error' in translation.keys():
            print("\t>>> Could not fetch translation. Check the logs.\n")
        print("\n\t>>> '{}'".format(translation['text']))
        print("")

    with MicrophoneStream(RATE, CHUNK, device_index=device_index) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
        client = speech.SpeechClient()
        streaming_config = create_configuration(input_lang)
        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        try:
            listen_print_loop(responses, callback=print_translation, debug=False)
        except OutOfRange as timeout:
            print("65 seconds time limit exceeded. Closing the stream.")
        except Exception as e:
            raise e


def create_argument_parser():
    parser = argparse.ArgumentParser(description='parse incoming')

    parser.add_argument('-v', '--verbose',
                        help="Be verbose. Sets logging level to INFO",
                        action="store_const",
                        dest="loglevel",
                        const=logging.INFO,
                        default=logging.INFO)

    parser.add_argument('-vv', '--debug',
                        help="Print lots of debugging statements. "
                             "Sets logging level to DEBUG",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG)

    parser.add_argument('-q', '--quiet',
                        help="Be quiet! Sets logging level to WARNING",
                        action="store_const",
                        dest="loglevel",
                        const=logging.WARNING)
    return parser


if __name__ == '__main__':

    cmdline_args = create_argument_parser().parse_args()
    logging.basicConfig(level=cmdline_args.loglevel)

    deepl_auth_key = os.getenv('DEEPL_KEY')

    if deepl_auth_key and credentials.valid():
        print("Google Cloud Speech credentials: VALID.")
        print("\n\tTo stop processing, say either: 'stop streaming', 'exit' or 'quit'\n")
        main(deepl_auth_key)
    else:
        print("Credentials not properly configured.")

