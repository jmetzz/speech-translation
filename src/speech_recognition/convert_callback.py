#!/usr/bin/env python3
import time
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.4
    r.non_speaking_duration = 0.3
    r.adjust_for_ambient_noise(source)


def callback(recognizer, audio):
    print("In callback")
    try:
        spoken = recognizer.recognize_google(audio, language="nl-NL")
        print("\tText: '{}'".format(spoken))
    except sr.UnknownValueError:
        print("\tCould not understand audio")
    except sr.RequestError as e:
        print("\tCould not request results from service; {0}".format(e))

print("Say something")
stop_listening = r.listen_in_background(m, callback, phrase_time_limit=0.6)
time.sleep(10)

print(">>>BEFORE")
# when stop_listening is called, it requests that the
# background listener thread stop
# stop_listening(wait_for_stop=False)
stop_listening(wait_for_stop=True)
print(">>>AFTER")

time.sleep(10)
print(">>>END")