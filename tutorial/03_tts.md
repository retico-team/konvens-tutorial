# Working with speech synthesis

Retico also comes with modules that perform speech synthesis (or text-to-speech). In this tutorial, you will use the [retico SpeechBrain TTS](https://github.com/retico-team/speechbraintts) to synthesize text into speech.

For this, you start with the basic setup of the incremental asr task:

```python

from retico import *

microphone = modules.MicrophoneModule(rate=16000)
asr = modules.Wav2VecASRModule(language="en")
printer = modules.TextPrinterModule()

microphone.subscribe(asr)
asr.subscribe(printer)

run(microphone)

print("Network is running")
input()

stop(microphone)
```

## Adding the SpeechBrain ASR module

In order to synthesize the text that is coming from the ASR module, you need to create a speechbraintts module and a speaker module first:

```python
tts = modules.SpeechBrainTTSModule(language="en")
speaker = modules.SpeakerModule(rate=22050)
```

The SpeechBrainTTSModule takes a language as an input parameter. Currently, only English (`en`) is available, but in the future, more languages will be added. The speaker module needs a sampling rate of `22050`, as the TTS outputs IUs with that rate.

The SpeechBrainTTSModule uses a caching functionality in order to synthesize text faster if it has already been synthesized. However, because synthesizing speech through a neural network is very time intensive, the process may take multiple seconds. That is why per default, the module is set only to synthesize speech once an utterance is completed and silence is detected.

## Connecting the modules

In order to add the TTS and the speaker to the network, they have to be connected together:

```python
asr.subscribe(tts)
tts.subscribe(speaker)
```

When the network is executed, the speech will be recognized and displayed by the TextPrinterModule. After an utterance is finished, the recognized text will be synthesized and sent to the speaker.

```diff
! If you execute the SpeechBrainTTSModule for the first time, the weights for the network will be downloaded, which might take a while.
```

## Exercises for you

- If your device is capable enough, try setting the `dispatch_on_finish` flag of the SpeechBrainTTSModule to `False`. This will incrementally generate the speech while you are still uttering the sentence. This might add some artifacts to the speech and works best on longer sentences.

---

[Next step: Adding dialogue management](04_dialogue.md)