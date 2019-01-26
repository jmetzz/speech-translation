#!/usr/bin/env python3
import argparse
import io
import logging
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
from utils import credentials

from dotenv import load_dotenv
load_dotenv()


def create_argument_parser():
    parser = argparse.ArgumentParser(description='parse incoming')

    parser.add_argument('-f', '--file',
                        help="The input file name",
                        required=True,
                        default=None,
                        type=str)

    parser.add_argument('-p', '--path',
                        help="The path to the input file",
                        required=False,
                        default='.',
                        type=str)

    parser.add_argument('-l', '--lang',
                        help="The language of the audio",
                        default='en-US',
                        type=str)

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


def transcribe(file_name, language='en-US', rate=16000):
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=rate,
            language_code=language)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    return response


if __name__ == '__main__':

    cmdline_args = create_argument_parser().parse_args()
    logging.basicConfig(level=cmdline_args.loglevel)

    if credentials.valid():
        file_name = os.path.join(cmdline_args.path, cmdline_args.file)
        language = cmdline_args.lang
        print("Google Cloud Speech credentials: VALID.")
        response = transcribe(file_name, language)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))
    else:
        print("Google Cloud credentials not properly configured.")
