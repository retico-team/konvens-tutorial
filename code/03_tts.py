#!/usr/bin/env python3

from retico import *

microphone = modules.MicrophoneModule(rate=16000)
asr = modules.Wav2VecASRModule(language="en")
printer = modules.TextPrinterModule()
tts = modules.SpeechBrainTTSModule(language="en")
speaker = modules.SpeakerModule(rate=22050)

microphone.subscribe(asr)
asr.subscribe(printer)
asr.subscribe(tts)
tts.subscribe(speaker)

run(microphone)

print("Network is running")
input()

stop(microphone)
