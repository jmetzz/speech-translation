#!/usr/bin/env python3

'''Simple demo application to convert audio to text'''
from os import path
from speech_recognition.converter import MicCaptureToText


def get_project_dir():
    path_array = path.dirname(path.realpath(__file__)).split('/')
    proj_root = "/".join(path_array[:len(path_array) - 1])
    return proj_root


if __name__ == '__main__':
    converter = MicCaptureToText(language="nl-NL")  # "sphinx"

    response = ""
    print("Using input from mic:")
    while response is not None and response != "stop":
        print("say something")
        transcription = converter.convert()
        response = transcription['text']
        print("Recognizer thinks you said '{}'".format(transcription))

    print("No more audio to transcribe")
