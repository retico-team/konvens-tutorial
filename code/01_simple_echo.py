#!/usr/bin/env python3

from retico import *

microphone = modules.MicrophoneModule()
speaker = modules.SpeakerModule()

microphone.subscribe(speaker)

run(microphone)

print("Network is running")
input()

stop(microphone)
