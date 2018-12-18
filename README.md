# Demo on speech to text with translation from Dutch to French

Recognizing speech requires audio input, and `SpeechRecognition` makes retrieving this 
input really easy. Instead of having to build scripts for accessing microphones and 
processing audio files from scratch, `SpeechRecognition` will have you up and running 
in just a few minutes.

This library acts as a wrapper for several popular speech APIs online and offline, 
and is thus extremely flexible. More specifically, it supports the 
*Google Speech Recognition* and *Google Cloud Speech API*, which I'm going to use for this demo. 
`SpeechRecognition` ships with a default API key for the *Google Speech Recognition* for testing purposes.

> Caution: The default key provided by SpeechRecognition is for testing purposes only, 
and Google may revoke it at any time. It is not a good idea to use the Google Web Speech API 
in production. Even with a valid API key, you’ll be limited to only 50 requests per day, 
and there is no way to raise this quota.


> Note: in case you need to use *Sphinx recognizer* you will need to install `PocketSphinx`
dependency

This demo is prepared to run on __OS X__. If you want to try it out on another platform, 
make sure you've got all the requirements correctly setup on your system before running the code.
Check the official documentation for the 
[installation instructions](https://pypi.org/project/SpeechRecognition/). 

I'm using conda environment to install all the python dependencies. Feel free to use another
strategy.  

## Requirements

In order to use `SpeechRecognition` we need to first install some extra dependencies.

- Python 3.3+ (required)
- PyAudio 0.2.11+ (required only if you need to use microphone input)
- Google API Client Library for Python
- PocketSphinx (only if you need to use the Sphinx recognizer)
- FLAC encoder (required only if the system is not x86-based Windows/Linux/OS X)
- DeepL API

### PyAudio (for microphone users)

PyAudio is required if and only if you want to use microphone input (Microphone).
If not installed, everything in the library will still work, except attempting to 
instantiate a `Microphone` object will raise an `AttributeError`.

 
> Note: PyAudio version 0.2.11+ is required, as earlier versions have known
memory management bugs when recording from microphones in certain situations.

If you are running on __OS X__, first install PortAudio using Homebrew:

    brew install portaudio

Then, specify `pyaudio` dependency in the `environment.yml` file.
 
> Note: if you are installing dependencies directly with pip, just run 
`pip install pyaudio`
    
For other platforms, check the [installation instructions](https://pypi.org/project/SpeechRecognition/).


### Google API Client Library 

The recommended way to install this API client is using `pip`. Thus, we only need to include 
it as a `pip` dependency in the `environment.yml` file.

> Note: Alternativelly, if you are not using conda environment just install with the regular
`pip3 install google-api-python-client`.

### PocketSphinx-Python (for Sphinx users)

> This package is required if and only if you want to use the Sphinx recognizer 
(`recognizer_instance.recognize_sphinx`).

This is the only recognizer that works offline. 

By default, SpeechRecognition's Sphinx functionality supports only US English. 
Additional language packs are also available, but not included due to 
the files being too large.

Additional languages available:

- International French
- Mandarin Chinese
- Italian

For __OS X__ and other POSIX systems, you'll need to build from source. Follow these instructions:

Install `swig`, `git` and `python3` in case you don't have them yet.
     
    $ brew install swig git python3

> [SWIG](http://www.swig.org/exec.html) is an interface compiler that connects programs 
written in C and C++ with scripting languages such as Perl, Python, Ruby, and Tcl.

    
Then include `pocketsphinx` as a pip dependency on your conda `environment.yml` file

    dependencies:
      - pyaudio
      - pip:
        - pocketsphinx

If this gives errors when importing the library in your program, check the 
installation instructions for __OS X__ under *“Building PocketSphinx-Python from source”* in 
[Notes on using PocketSphinx](https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst).


### FLAC encoder

Since I'm using __OS X__, nothing needs to be done.

The official documentation states:

> A FLAC encoder is required to encode the audio data to send to the API. 
If using Windows (x86 or x86-64), __OS X__ (Intel Macs only, OS X 10.6 or higher), 
or Linux (x86 or x86-64), this is already bundled with this library - 
you do not need to install anything.


## DeepL API

>TBD


## References

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Notes on using PocketSphinx](https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst)
- [Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/)
- [Code examples](https://github.com/Uberi/speech_recognition/tree/master/examples)