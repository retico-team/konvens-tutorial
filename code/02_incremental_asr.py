#!/usr/bin/env python3

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
