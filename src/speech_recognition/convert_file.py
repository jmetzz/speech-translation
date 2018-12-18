#!/usr/bin/env python3

'''Simple demo application to convert audio to text'''
from os import path

from speech_recognition.converter import AudioFileToText


def get_project_dir():
    path_array = path.dirname(path.realpath(__file__)).split('/')
    proj_root = "/".join(path_array[:len(path_array) - 1])
    return proj_root


# use the audio file as the audio source
if __name__ == '__main__':
    converter = AudioFileToText("google")  # "sphinx"

    AUDIO_FILE = path.join(path.realpath(get_project_dir()),
                           "resources",
                           "harvard.wav")
    print(
        "Recognizer thinks you said '{}'".format(converter.convert(AUDIO_FILE)))
