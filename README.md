# Demo on speech transcription and translation

> This demo is prepared to run on __OS X__. If you want to try it out on another platform,
make sure you've covered the requirements. 

## Requirements

In order to use `SpeechRecognition` we need to first install some extra dependencies.

- Python 3.3+ (required)
- PyAudio 0.2.11+ (required only if you need to use microphone input)
- FLAC encoder (required only if the system is not x86-based Windows/Linux/OS X)

### PyAudio

PyAudio is required to use microphone input (Microphone).
 
> Note: PyAudio version 0.2.11+ is required, as earlier versions have known
memory management bugs when recording from microphones in certain situations.

If you are running on __OS X__, first install PortAudio using Homebrew:

    brew install portaudio

Then, specify `pyaudio` dependency in the `environment.yml` file.
 
> For other platforms, check the [installation instructions](https://pypi.org/project/SpeechRecognition/).


### FLAC encoder

Since I'm using __OS X__, nothing needs to be done.

The official documentation states:

> A FLAC encoder is required to encode the audio data to send to the API. 
If using Windows (x86 or x86-64), __OS X__ (Intel Macs only, OS X 10.6 or higher), 
or Linux (x86 or x86-64), this is already bundled with this library - 
you do not need to install anything.


### Credentials

To run the examples make sure you have prepared the following required environment variables:

* GOOGLE_APPLICATION_CREDENTIALS
* DEEPL_KEY

Just add into your project a `.env` file with these variables defined. 
They will be automatically loaded by the program upon load time.

The content of the file should be something like this:

```python
export GOOGLE_APPLICATION_CREDENTIALS=path/to/your-google-credential-file.json
export DEEPL_KEY=value-of-your-deepl-authorization-key
```

The `export` key word is not required, but comes handy in case you want to export these variables 
to your current shell session. In such a case you only need to `source` the file.

The google credentials file should look like this:

```json
{
  "type": "service_account",
  "project_id": "your-project_id",
  "private_key_id": "your private key id",
  "private_key": "your private key value",
  "client_email": "your client email",
  "client_id": "your client id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your cert url"
}
```

You can generate this file on Google Cloud platform. Just follow the instructions on 
[Setup credentials](https://cloud.google.com/docs/authentication/production#auth-cloud-implicit-python)
 
You can verify if your credentials are correct configured by running the `credentials.py` module on 
`src/main/python/utils`.
 
> If running from IntelliJ IDEA make sure you tick the option 'Emulate terminal in output console'
from the 'Run Configuration'.


## Executing the examples:

I'm using conda environment to install all the python dependencies. Feel free to use another
strategy.  

Thus, you must first create the conda environment as follows:

```bash
$ conda env create -f environment.yml
$ conda activate speech-translation
```

> I've experienced some issues to install `google-cloud-speech` with conda. For some reason that I could
not understand yet, sometimes this package and its dependencies are not installed. If this happens, 
when you run the `translate_stream_demo.py` you will see an error with a message similar to 
'python No module named 'grpc''. In this case, activate the environment and 
install `google-cloud-speech` manually via `pip install google-cloud-speech`.
  

Now you only need to execute the python modules as usual, such as:

```bash
$ cd src/main/python
$ python translate_stream_demo.py
```


# Quick guide to speech recognition with python and Google Speech API

> This section is a working in progress

## Introduction 

Speech must be converted from physical sound to an electrical signal with a microphone, 
and then to digital data with an analog-to-digital converter. 
 
Most modern speech recognition systems rely on *Hidden Markov Model* (HMM), an approach that assumes 
a speech signal can be reasonably approximated as a stationary process when viewed on 
a short enough timescale (say, ten milliseconds). That is, a process in which 
statistical properties do not change over time.

Typically the speech signal is divided into 10-millisecond fragments, which is then mapped to 
a vector of real numbers (coefficients). The final output of the HMM is a sequence of these vectors.

To decode the speech into text, groups of vectors are matched to one or more phonemes.
This process requires training, since the sound of a phoneme varies from speaker to speaker. 

In many modern speech recognition systems, neural networks are used to simplify the 
speech signal using techniques for feature transformation and dimensionality reduction 
before HMM recognition. Voice activity detectors (VADs) are also used to reduce an audio signal 
to only the portions that are likely to contain speech.

> Note: check the __Glossary__ section in case you get confused with the terms 


## Recognition process

The common way to recognize speech is the following: we take a waveform, 
split it at utterances by silences and then try to recognize what’s being said in each utterance. 
To do that, we want to take all possible combinations of words and try to match them with the audio.
We then choose the best matching combination.

There are some important concepts in this matching process:

. Features,
. Model, and
. Matching process.


Features are numbers or coefficients calculated from speech usually by dividing the speech into frames.
Then from each frame, typically of 10 milliseconds length, 39 coefficients that represent the speech 
are extracted. These coefficients represent then feature vector. 

The model describes some mathematical objects that shares
common attributes of the spoken word. The model of speech is usually a 
[Hidden Markov Model](http://en.wikipedia.org/wiki/Hidden_Markov_model) 
or HMM. It’s a generic model that describes a black-box communication channel. 
A process described as a sequence of states which change each other with a 
certain probability. This model is intended to describe any sequential process like speech. 
HMMs have been proven to be really practical for speech decoding.

The matching is a optimized search process. Since it is prohibitive to compare all feature vectors 
with all possible models, the search is often optimized by applying many tricks. 
At any points we maintain the best matching variants and extend them as time goes on, 
producing the best matching variants for the next frame.

According to the speech structure, three models are used in speech recognition to do the match: an __acoustic model__ 
contains acoustic properties for each senone. There are context-independent models that contain 
properties (the most probable feature vectors for each phone) and context-dependent ones 
(built from senones with context); a __phonetic dictionary__ contains a mapping from words to phones; 
and a __language model__ ...


## Google Cloud Speech-to-Text API

Speech-to-Text has three main methods to perform speech recognition:

- Synchronous Recognition (REST and gRPC) sends audio data to the Speech-to-Text API, 
performs recognition on that data, and returns results after all audio has been processed. 
Synchronous recognition requests are limited to audio data of 1 minute or less in duration.

- Asynchronous Recognition (REST and gRPC) sends audio data to the Speech-to-Text API 
and initiates a Long Running Operation. Using this operation, you can periodically poll for 
recognition results. Use asynchronous requests for audio data of any duration up to 180 minutes.

> Asynchronous calls, in which you send both the configuration and audio within a single request, 
calling the streaming Speech API requires sending multiple requests.

- __Streaming Recognition__ (gRPC only) performs recognition on audio data provided within a 
gRPC bi-directional stream. Streaming requests are designed __for real-time recognition__ purposes, 
such as __capturing live audio from a microphone__. Streaming recognition provides interim results 
while audio is being captured, allowing result to appear, for example, while a user is 
still speaking.

We focus on __Streaming Recognition__, since our case requires real time translation from audio.

The first `StreamingRecognizeRequest` must contain a configuration of type `StreamingRecognitionConfig` 
without any accompanying audio. Subsequent `StreamingRecognizeRequests` sent over the same stream will 
then consist of consecutive frames of raw audio bytes.

Configuration fields:

- `config` - (required) contains configuration information for the audio, of type 
`RecognitionConfig`.

- `single_utterance` - (optional, defaults to `false`) indicates whether this request should 
automatically end after speech is no longer detected. If set, Speech-to-Text will detect pauses, 
silence, or non-speech audio to determine when to end recognition. __If not set, the stream will 
continue to listen and process audio until either the stream is closed directly__, or the stream's 
limit length has been exceeded. Setting `single_utterance` to true is useful for 
processing voice commands.

- `interim_results` - (optional, defaults to `false`) indicates that this stream request should 
return temporary results that may be refined at a later time (after processing more audio). 
Interim results will be noted within responses through the setting of `is_final` to `false`.

to be continued ....



We can use one of several pre-defined machine learning models to transcribe your audio file.
Google has trained these speech recognition models for specific audio types and sources, such as:
 `video`, `phone_call`, `command_and_search` and `default`.

It is also possible to improve the speech recognition quality by using `phrase hints` through a 
`speechContext` object. This context can hold a list of phrases to act as "hints" to the recognizer.
Such additional phrases may be particularly useful if the supplied audio contains noise or 
the contained speech is not very clear. It can also be used to add additional words to the 
vocabulary of the recognition task.

> Note: In general, be sparing when providing speech context hints. Better recognition accuracy 
can be achieved by limiting phrases to only those expected to be spoken.

  
  
## Glossary

> To be done

- waveform:
- utterances:
- feature:
- feature vector:
- frame: typically 10 miliseconds length section of the audio
- phone:
- diphone:
- model:
- senone:



## Reference material

- [Python Speech Recognition tutorial](https://realpython.com/python-speech-recognition/)
- [Google Cloud Speech-to-Text AI](https://cloud.google.com/speech-to-text/)
    - [Google Cloud Speech-to-Text Basics](https://cloud.google.com/speech-to-text/docs/basics)
    - [Setup credentials](https://cloud.google.com/docs/authentication/production#auth-cloud-implicit-python)
    - [Example applications](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/speech/cloud-client)
- [IBM Speech to Text](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/speech-to-text.html)
- [Snowboy Hotword Detection](https://snowboy.kitt.ai/)
- [Microsoft Dictate - MS Office add-in](https://www.microsoft.com/en-us/garage/profiles/dictate/)
- [Microsoft Garage - MS Office add-in](https://www.microsoft.com/en-us/garage/profiles/presentation-translator/)
- [DeepL](https://www.deepl.com)
- [Open Speech Repository](http://www.voiptroubleshooter.com/open_speech/index.html).
- [Code examples](https://github.com/Uberi/speech_recognition/tree/master/examples)