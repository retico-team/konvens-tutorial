#!/usr/bin/env python3

from retico import *

msg = []


def word_remover(update_message):
    global msg
    for x, ut in update_message:
        if x.text == "green":
            x.text = "blue"
            x.payload = "blue"
        if ut == UpdateType.ADD:
            msg.append(x)
        if ut == UpdateType.REVOKE:
            msg.remove(x)
    txt = ""
    committed = False
    for x in msg:
        txt += x.text + " "
        committed = committed or x.committed
    print(" " * 100, end="\r")
    print(f"{txt}", end="\r")
    if committed:
        msg = []
        print("")


microphone = modules.MicrophoneModule(rate=16000)
asr = modules.Wav2VecASRModule(language="en")
callbackmodule = modules.CallbackModule(word_remover)
tts = modules.SpeechBrainTTSModule(language="en")
speaker = modules.SpeakerModule(rate=22050)

microphone.subscribe(asr)
asr.subscribe(callbackmodule)
asr.subscribe(tts)
tts.subscribe(speaker)

run(microphone)

print("Network is running")
input()

stop(microphone)
