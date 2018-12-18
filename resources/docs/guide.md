# Guide to Speech Recognition with python


## Introduction 

Speech must be converted from physical sound to an electrical signal with a microphone, 
and then to digital data with an analog-to-digital converter
 
Most modern speech recognition systems rely on what is known as a Hidden Markov Model (HMM). 
This approach works on the assumption that a speech signal, when viewed on a short enough timescale
(say, ten milliseconds), can be reasonably approximated as a stationary process—that is, 
a process in which statistical properties do not change over time.

Typically the speech signal is divided into 10-millisecond fragments, which is then mapped to 
a vector of real numbers (cepstral coefficients) with usually dimension as low as 10, but sometimes 
32 or more. The final output of the HMM is a sequence of these vectors.

To decode the speech into text, groups of vectors are matched to one or more phonemes.
This requires training, since the sound of a phoneme varies from speaker to speaker. 

In many modern speech recognition systems, neural networks are used to simplify the 
speech signal using techniques for feature transformation and dimensionality reduction 
before HMM recognition. Voice activity detectors (VADs) are also used to reduce an audio signal 
to only the portions that are likely to contain speech.

> Note: check the __Glossary__ section in case you get confused with the terms 


## Recognition process

The common way to recognize speech is the following: we take a waveform, 
split it at utterances by silences and then try to recognize what’s being said in each utterance. 
To do that, we want to take all possible combinations of words and try to match them with the audio.
We choose the best matching combination.

There are some important concepts in this matching process. First of all it’s the concept of features. 
Since the number of parameters is large, we are trying to optimize it. Numbers that are calculated 
from speech usually by dividing the speech into frames. Then for each frame, typically of 
10 milliseconds length, we extract 39 numbers that represent the speech. 
That’s called a feature vector. The way to generate the number of parameters is a subject of 
active investigation, but in a simple case it’s a derivative from the spectrum.

Second, it’s the concept of the model. A model describes some mathematical object that gathers 
common attributes of the spoken word. In practice, for an audio model of senone it is the 
gaussian mixture of it’s three states - to put it simple, it’s the most probable feature vector. 
From the concept of the model the following issues raise:

- how well does the model describe reality?
- can the model be made better of it’s internal model problems? and
- how adaptive is the model if conditions change?

The model of speech is called [Hidden Markov Model](http://en.wikipedia.org/wiki/Hidden_Markov_model) 
or HMM. It’s a generic model that describes a black-box communication channel. 
In this model process is described as a sequence of states which change each other with a 
certain probability. This model is intended to describe any sequential process like speech. 
HMMs have been proven to be really practical for speech decoding.

Third, it’s a matching process itself. Since it would take longer than universe existed to 
compare all feature vectors with all models, the search is often optimized by applying many tricks. 
At any points we maintain the best matching variants and extend them as time goes on, 
producing the best matching variants for the next frame.

## Models

According to the speech structure, three models are used in speech recognition to do the match:

An __acoustic model__ contains acoustic properties for each senone. 
There are context-independent models that contain properties (the most probable feature vectors 
for each phone) and context-dependent ones (built from senones with context).

A __phonetic dictionary__ contains a mapping from words to phones. This mapping is not very 
effective. For example, only two to three pronunciation variants are noted in it. 
However, it’s practical enough most of the time. The dictionary is not the only method for 
mapping words to phones. You could also use some complex function learned with a 
machine learning algorithm.

A __language model__ 


## Google Cloud Speech-to-Text API

Speech-to-Text has three main methods to perform speech recognition:

- Synchronous Recognition (REST and gRPC) sends audio data to the Speech-to-Text API, 
performs recognition on that data, and returns results after all audio has been processed. 
Synchronous recognition requests are limited to audio data of 1 minute or less in duration.

- Asynchronous Recognition (REST and gRPC) sends audio data to the Speech-to-Text API 
and initiates a Long Running Operation. Using this operation, you can periodically poll for 
recognition results. Use asynchronous requests for audio data of any duration up to 180 minutes.

- __Streaming Recognition__ (gRPC only) performs recognition on audio data provided within a 
gRPC bi-directional stream. Streaming requests are designed __for real-time recognition__ purposes, 
such as __capturing live audio from a microphone__. Streaming recognition provides interim results 
while audio is being captured, allowing result to appear, for example, while a user is 
still speaking.


We focus on __Streaming Recognition__, since our case requires real time translation from audio.


Speech-to-Text can use one of several machine learning models to transcribe your audio file.
Google has trained these speech recognition models for specific audio types and sources.
The available models are: `video`, `phone_call`, `command_and_search` and `default`.

Google also provides a way to improve the speech recognition by using `phrase hints` through a 
`speechContext` object. This context can hold a list of phrases to act as "hints" to the recognizer.
Such additional phrases may be particularly useful if the supplied audio contains noise or 
the contained speech is not very clear. It can also be used to add additional words to the 
vocabulary of the recognition task.

> Note: In general, be sparing when providing speech context hints. Better recognition accuracy 
can be achieved by limiting phrases to only those expected to be spoken.



## Streaming Recognition 

Asynchronous calls, in which you send both the configuration and audio within a single request, 
calling the streaming Speech API requires sending multiple requests.

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
  
  
## Glossary

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
- SpeechRecognition python module
    - [PyPi web page](https://pypi.org/project/SpeechRecognition/)
    - [Github repository](https://github.com/Uberi/speech_recognition)
    - [Library Reference](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst)
- CMUSphinx
    - [Documentation](https://cmusphinx.github.io/wiki/)
    - [Tutorial For Developers](https://cmusphinx.github.io/wiki/tutorial/)
    - [Acoustic and Language Models](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/)
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

