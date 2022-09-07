# Working with an incremental speech recognition

Retico comes with modules that perform incremental speech recognition. The [retico GoogleASR](https://github.com/retico-team/retico-googleasr) module provides a fast speech recognition in the form of a cloud based service. However, using this module requires a google account with payment enabled. That is why we use the [retico Wav2Vec ASR](https://github.com/retico-team/retico-wav2vecasr) module that uses deep learning to translate the speech into text.

Similar to the echo example, we start by importing retico and creating a microphone module:

```python
from retico import *

microphone = modules.MicrophoneModule(rate=16000)
```

Here, we set the sampling rate to 16 kHz, as the Wav2Vec speech recognition expects this rate. We could set the sampling rate to another value, but the `Wav2VecASRModule` would then convert the audio back to 16 kHz.

## Using the Wav2Vec ASR

Using the Wav2Vec ASR is simple: the module can be created and included in the network like any other module:

```python
asr = modules.Wav2VecASRModule(language="en")
```

The `language` option can be set to any of the following languages: `en` for English, `de` for German, `fr` for French, and `es` for Spanish. Additional languages can be set manually.

As Wav2Vec is a large neural network, it takes some time for a prediction to be made. Depending on the capabilities of your device, it may take a few second for a prediction to be made.

## Visualizing the result

In order to visualize the output of the Wav2VecASRModule, we need to print out the incremental units the module is producing. For this, a `TextPrinterModule` is available.

```python
printer = modules.TextPrinterModule()
```

This module collects all incoming incremental units (words) and prints them out in a single line, updating the text as new IUs are coming in. Once a text has been *committed*, the text printer module clears the buffer and starts over on a new line.

## Connecting the network and testing it

Finally, the modules have to be connected in order for the incremental units to pass between the modules.

```python
microphone.subscribe(asr)
asr.subscribe(printer)
```

Then, the network can be executed like this:

```python
run(microphone)

print("Network is running")
input()

stop(microphone)
```
Running this code will allow you to speak into the microphone and the recognized text will be printed to the console. As the speech recognition might be slow on your machine, the incrementality of the system works better with longer sentences.

```diff
! If you execute the Wav2VecASRModule for the first time, the weights for the network will be downloaded, which might take a while.
```

## Exercises for you

- Try using another language in the speech recognizer, by using one of the language codes `en`, `de`, `fr`, `es`.
- Try changing the sampling rate of the microphone to a value lower than 16000 (e.g., 8000). The quality of the asr decreases as there is less information available. (You need to set the `framerate` of the Wav2VecASRModule accordingly).
- Try adding a speaker output and connect it with the microphone module

---

[Next step: Working with speech synthesis](03_tts.md)