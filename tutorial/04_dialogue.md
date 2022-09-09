# Adding dialogue management

Now that you have a system that is able to record, automatically recognize and then resynthesize speech, let's add some simple dialogue processing. In this step, you will implement your own incremental module called the `WordChangerModule`. This module will accept `TextIU`s as input and also produce `TextIU`s. When the module is initialized, it will take a map of words and what they should be changed into. For example, the module could obtain `{"green": "blue"}` as an argument and would always change the word "green" to "blue".

## Creating the skeleton of a new incremental module

In order to create a new incremental module, you need to create a class that inherits from the `AbstractModule` class:

```python
from retico import *

class WordChangerModule(AbstractModule):
    @staticmethod
    def name():
        return "Word Changer Module"

    @staticmethod
    def description():
        return "Module that changes specific words."

    @staticmethod
    def input_ius():
        return [ius.TextIU]

    @staticmethod
    def output_iu():
        return ius.TextIU
```

Every incremental module **has to** implement four static methods:

 - the `name()` method, that returns a human-readable name of the module,
 - the `description()` method, that returns a human-readable description,
 - the `input_iu()` method, that returns a list of incremental unit *classes* that the module can take as an input (can be an empty list, e.g., for the `MicrophoneModule`),
 - and the `output_iu()` method, that returns the incremental unit *class* that the module produces (can be `None`, e.g., for the `SpeakerModule`).

All these methods are *static* (`@staticmethod` before the declaration of the method), which means that the methods are available without instantiating the module. As an example, you can call the methods like this:

```python
print(WordChangerModule.description())
```
## Writing an initializer

In order to hand the word map (mapping the words to replace with their respective replacement words) to the module, you need to write an `__init__` function.

For this, you can add the following code to the class:

```python
    def __init__(self, word_map, **kwargs):
        super().__init__(**kwargs)
        self.word_map = word_map
```

This method declares that the initializer of the `WordChangerModule` takes the `word_map` and additional arguments (`**kwargs`). The line `super().__init__(**kwargs)` makes sure the `AbstractModule` that it inherits from is properly initialized, and it passes the *additional arguments* (`**kwargs`) down to that initializer. These additional arguments may contain some metadata for the module, but for now, you do not have to care about that part.

Finally, the code sets the class variable `self.word_map` to the word map that is given as the parameter. You can try the initializer in the following way:

```python
word_changer = WordChangerModule(word_map={"green": "blue", "yellow": "black"})
print(word_changer.word_map)
```

## Changing the words

To change the words in the incoming incremental units accordingly, you need to implement one last method called `process_update`. This method is the main processing part of every incremental module.

Whenever a new update message (containing one or multiple incremental units with their respective update types) arrives at the left buffer of your module, the retico framework will call the `process_update` method with the update message. The method then is able to process the new information, add new incremental modules, or revoke them. Finally, the method can return it's own update message, containing incremental units that were created or revoked based on the incoming IUs (the method can also return `None` if no updates are necessary).

For your `WordChangerModule` the method looks like this:

```python
    def process_update(self, update_message):
        new_update_message = UpdateMessage()
        for incremental_unit, update_type in update_message:
            # When the incremental unit is in the list of words
            if incremental_unit.text in self.word_map.keys():
                # Replace the text with the respective word
                incremental_unit.text = self.word_map[incremental_unit.text]
            # Add incremental unit to the new update message and keep the update type
            new_update_message.add_iu(incremental_unit, update_type)
        return new_update_message
```

First, the code creates a `new_update_message`, which will collect all incremental units that will be returned for the given input. Because the module only replaces words, it will always have the same number of incoming IUs as it has outgoing IUs.

The for-loop iterates over every `incremental_unit`-`update_type`-pair in the `udate_message`. The code then checks if the word of the current incremental unit is contained in the list of words that should be replaced (`self.word_map.keys()`). If so, the text of the IU is replaced with the respective word from the word map. Finally, the IU is added to the `new_update_message`, with the same update_type.

In the last step, the `new_update_message` is returned. The retico framework will take this update message and send it to all connected modules.

## Creating the network

With the new incremental module created, you can now build a network with it:

```python
microphone = modules.MicrophoneModule(rate=16000)
asr = modules.Wav2VecASRModule(language="en")
wordchanger = WordChangerModule(word_map={"green": "blue"})
printer = modules.TextPrinterModule()
tts = modules.SpeechBrainTTSModule(language="en")
speaker = modules.SpeakerModule(rate=22050)

microphone.subscribe(asr)
asr.subscribe(wordchanger)
wordchanger.subscribe(printer)
wordchanger.subscribe(tts)
tts.subscribe(speaker)

run(microphone)

print("Network is running")
input()

stop(microphone)
```

Again, the microphone is connected the automatic speech recognition. The ASR is then sending its output to your new wordchanger module. In this example, the word "green" is replaced with "blue". The output is then sent to the printer module for you to read the changed text and the TTS module to synthesize the result. Finally, the output of the TTS is sent to the speaker.


## Exercises for you

- Try larger word maps that change almost every word in your input sentence
- Modify the `WordChangerModule` to reverse every incoming word (e.g., change "hello" to "olleh") and listen to the TTS struggle with the result.

---

[Next step: Creating an incremental translation system](05_translation.md)