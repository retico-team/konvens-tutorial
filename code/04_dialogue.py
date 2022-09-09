#!/usr/bin/env python3

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

    def __init__(self, word_map, **kwargs):
        super().__init__(**kwargs)
        self.word_map = word_map

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
