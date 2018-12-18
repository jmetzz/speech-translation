import speech_recognition as sr


class RecognizerFactory:
    _registry = ["google", "sphinx"]

    @classmethod
    def of(cls, name):
        if name not in cls._registry:
            raise ValueError("`recognizer` not registered. Use {}'"
                             .format(cls._registry))
        recognizer = sr.Recognizer()
        if name == 'google':
            return recognizer, recognizer.recognize_google
        else:
            return recognizer, recognizer.recognize_sphinx

    @classmethod
    def recognizers(cls):
        return list(cls._registry)


class Speech2TextConverter:
    def __init__(self, recognizer="google", language="en-US"):
        self._recog_name = recognizer
        self._language = language
        self._recognizer, self._transcriber = RecognizerFactory.of(recognizer)

    def handle(self, audio, debug=False):
        """Transcribe speech from recorded from `microphone`.

            Returns a dictionary with three keys:
            "success": a boolean indicating whether or not the API request was
                       successful
            "error":   `None` if no error occurred, otherwise a string containing
                       an error message if the API could not be reached or
                       speech was unrecognizable
           "stack trace": `None` if no error occurred, otherwise the exception
                        stack trace
            "transcription": `None` if speech could not be transcribed,
                       otherwise a string containing the transcribed text
        """
        response = {
            "success": True,
            "error": None,
            "stack trace": None,
            "text": None
        }
        try:
            response['text'] = self._transcriber(audio,
                                                 language=self._language,
                                                 show_all=debug)
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
            response['stack trace'] = "Recognizer error; {0}".format(e)
        finally:
            return response


class MicCaptureToText(Speech2TextConverter):

    def __init__(self, name='google', language="en-US", index=None,
            adjust_duration=0.5):
        self._device = index
        self._adjust_duration = adjust_duration

        super(MicCaptureToText, self).__init__(name, language)

    def convert(self, debug=False):
        audio = self._audio_from_mic()
        return self.handle(audio, debug)

    def _audio_from_mic(self):
        # use the default microphone as the audio source
        # listen for the first phrase and extract it into audio data

        # If your system has no default microphone or you want to use a
        # microphone other than the default, you will need to specify which
        # one to use by supplying a device index.
        # You can get a list of microphone names by calling the
        # list_microphone_names() static method of the Microphone class.
        with sr.Microphone(device_index=self._device) as mic:
            # Microphone class is a context manager.
            # You can capture input from the microphone using the listen()
            # method of the Recognizer class
            # This method takes an audio source as its first argument and
            # records input from the source until silence is detected.
            # To handle ambient noise, you’ll need to use the
            # adjust_for_ambient_noise() method of the Recognizer class.
            # It is strongly recommended to do it.
            # The SpeechRecognition documentation recommends using
            # a duration no less than 0.5 seconds.
            self._recognizer. \
                adjust_for_ambient_noise(mic, duration=self._adjust_duration)

            return self._recognizer.listen(mic)


class AudioFileToText(Speech2TextConverter):
    def convert(self, audio_file, debug=False):
        audio = self._audio_from_file(audio_file)
        return self.handle(audio, debug)

    def _audio_from_file(self, audio_file):
        # The context manager opens the file and reads its contents,
        # storing the data in an AudioFile instance called source
        with sr.AudioFile(audio_file) as source:
            # Read the entire audio file
            # records the data from the entire file into an AudioData instance

            # The ambient noise in an audio file can cause problems
            # and must be addressed in order to maximize the accuracy
            # of speech recognition.
            # The adjust_for_ambient_noise() method reads the first second of
            # the file stream and calibrates the recognizer to the noise level
            # of the audio. Hence, the portion of the stream that is consumed
            # before you call record() to capture the data can be controlled
            # by the parameter 'duration' on adjust_for_ambient_noise method
            # self._recognizer.adjust_for_ambient_noise(source)
            return self._recognizer.record(source)
