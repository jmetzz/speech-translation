#!/usr/bin/env python3

import re
import sys

import pyaudio
from prompt_toolkit import prompt

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Audio recording parameters
from gcloud.stream.microphone import MicrophoneStream
from translation import Translator

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def listen_print_loop(responses, callback=print, debug=False):
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
            callback(transcript)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(stop streaming|exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def show_translation(text):
    print("\t >>> Translation: '{}'".format(Translator.handle(text)))


def choose_device():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get(
                'maxInputChannels')) > 0:
            print("[{}] {}".format(i,
                                   p.get_device_info_by_host_api_device_index(0,
                                                                              i).get(
                                       'name')))
    return prompt("Which device do you want to use? ")


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    # language_code = 'en-US'  # a BCP-47 language tag
    language_code = 'nl-NL'  # a BCP-47 language tag

    device_index = int(choose_device())
    print(device_index)

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
            # Enable automatic punctuation
            enable_automatic_punctuation=True)
    streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

    with MicrophoneStream(RATE, CHUNK, device_index=device_index) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses, callback=show_translation, debug=True)


if __name__ == '__main__':
    main()
