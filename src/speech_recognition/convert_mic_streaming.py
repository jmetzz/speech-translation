#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from threading import Thread

try:
    from queue import Queue  # Python 3 import
except ImportError:
    from Queue import Queue  # Python 2 import

import speech_recognition as sr

r = sr.Recognizer()
audio_queue = Queue()


def recognize_worker():
    # this runs in a background thread
    while True:
        # retrieve the next audio processing job from the main thread
        audio = audio_queue.get()
        if audio is None:
            break  # stop processing if the main thread is done

        # received audio data, now we'll recognize it using
        # Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("You said: '{}'".
                  format(r.recognize_google(audio)))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # mark the audio processing job as completed in the queue
        audio_queue.task_done()


# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()

# repeatedly listen for phrases and put the resulting audio on the audio
# processing job queue
#
# r.listen(source):
#   signature -> listen(self, source,
#                       timeout=None,
#                       phrase_time_limit=None,
#                       snowboy_configuration=None):

# Records a single phrase from ``source``(an ``AudioSource`` instance)
# into an ``AudioData`` instance, which it returns.
#
# Note: Energy level threshold is used to differentiate between speech
# and silence. Values below this threshold are considered silence,
# and values above this threshold are considered speech.
#
# This is done by waiting until the audio has an energy above
# ``recognizer_instance.energy_threshold`` (the user has started speaking),
# and then recording until it encounters ``recognizer_instance.pause_threshold``
# seconds of non-speaking or there is no more audio input. The ending
# silence is not included.
#
# The ``timeout`` parameter is the maximum number of seconds that this will
# wait for a phrase to start before giving up and throwing an
# ``speech_recognition.WaitTimeoutError`` exception.
# If ``timeout`` is ``None``, there will be no wait timeout.
#
# The ``phrase_time_limit`` parameter is the maximum number of seconds that
# this will allow a phrase to continue before stopping and returning the
# part of the phrase processed before the time limit was reached.
# The resulting audio will be the phrase cut off at the time limit.
# If ``phrase_timeout`` is ``None``, there will be no phrase time limit.
#
# The ``snowboy_configuration`` parameter allows integration with
# `Snowboy <https://snowboy.kitt.ai/>`__, an offline, high-accuracy,
# power-efficient hotword recognition engine. When used, this function will
# pause until Snowboy detects a hotword, after which it will unpause.
# This parameter should either be ``None`` to turn off Snowboy support,
# or a tuple of the form ``(SNOWBOY_LOCATION, LIST_OF_HOT_WORD_FILES)``,
# where ``SNOWBOY_LOCATION`` is the path to the Snowboy root directory,
# and ``LIST_OF_HOT_WORD_FILES`` is a list of paths to Snowboy hotword
# configuration files (`*.pmdl` or `*.umdl` format).
#
# This operation will always complete within ``timeout + phrase_timeout``
# seconds if both are numbers, either by returning the audio data,
# or by raising a ``speech_recognition.WaitTimeoutError`` exception.

with sr.Microphone(device_index=2) as mic:
    # Some sr.Recognizer options to consider in order to handle noisy
    #
    # energy_threshold # type: float
    # dynamic_energy_threshold # type: bool (default: True)
    # dynamic_energy_adjustment_damping # type: float (change is not recommended)
    # dynamic_energy_adjustment_ratio #type: float (times louder than ambient noise)
    # pause_threshold #type: float (in seconds)
    # operation_timeout # type: Union[float, None] (in seconds)
    # non_speaking_duration

    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.4
    r.non_speaking_duration = 0.3
    # r.adjust_for_ambient_noise(source)
    try:
        while True:
            # timeout: maximum number of seconds that this will wait for a
            # phrase to start before giving up
            # phrase_time_limit: maximum number of seconds that this will
            # allow a phrase to continue before stopping
            audio_queue.put(r.listen(mic))
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
print("No more audio to transcribe")