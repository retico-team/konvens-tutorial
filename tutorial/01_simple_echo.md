# Creating a simple echo network

The most simple incremental network is an echo network that records audio from the microphone of you laptop, packages the incoming data into incremental units, and finally outputs the audio to your speakers.

```diff
- Building this echo network may create a feedback loop, resulting in loud feedback noise! We recommend to use headphones to avoid this.
```

## Importing retico

The easiest way to work with retico is to import everything from its module:

```python
from retico import *
```

This way all the incremental modules, incremental units and auxiliary functionality is available.

## Creating a microphone module

Retico provides all available incremental modules in the `modules` member for easy access:

```python
microphone = modules.MicrophoneModule()
```

This creates a microphone with standard settings, such as a `frame_length` of `0.02`, which means that in each incremental unit 20 milliseconds of audio are transmitted. The sampling rate (`rate`) is per default set to `44100` which results in clean fullband audio. The `sample_width` (i.e., the size of one sample of audio in bytes) is set to `2`. These parameters may be changed, but for now we will leave them in the default setting.

## Creating a speaker module

The speaker module can be created with:

```python
speaker = modules.SpeakerModule()
```

Again, the speaker module has the default parameters `rate` and `sample_width`. The length of one incremental unit is not specified, as the speaker just outputs any length of audio that is put in its left buffer.

## Connecting the modules

When executing these two modules, the microphone modules will continuously produce `AudioIU`s and puts them in its right buffer (output). The speaker module will expect `AudioIU`s to be placed in its left buffer (input) and will put the contents to the speakers of your device.

However, for the audio IUs to travel from one module to the other, the modules need to be *connected* first. To connect the right buffer of the microphone module to the left buffer of the speaker module, use the `subscribe` method of the microphone module:

```python
microphone.subscribe(speaker)
```

Now, when both modules are being executed, the IUs that the microphone produces will be sent to the left buffer of the speaker.

## Executing the network

An incremental module can be executed by calling its `run` method and it can be stopped by calling its `stop` method. For our small network, this is very short:

```python
microphone.run()
speaker.run()

print("Network is running")
input()

microphone.stop()
speaker.stop()
```

As the modules each run in their own *thread*, the python code does not wait for anything to happen and would just immediately stop the modules again. In order to wait for a user input, the `input()` function of python waits for a user input followed by pressing the return key. That way the modules will run indefinitely and only stop once you pressed the enter key.

For larger networks that contain many more incremental modules, running and stopping all of the modules takes up a lot of space, and maybe you forget to run one module. That is why retico provides the `run()` and the `stop()` function:

```python
run(microphone)

print("Network is running")
input()

stop(microphone)
```

These methods only require one module in order to execute and stop the whole network. Retico automatically figures out which modules are belonging to the network and will execute or stop them. That means, if you exchange the `microphone` with `speaker` in the code above, the behavior would stay exactly the same.

```diff
! Sometimes Bluetooth devices add some delay on the audio data that is received by the MicrophoneModule.
```

## Exercises for you

That's it! Now you should be able to hear your own voice when running the network. Don't forget to use headphones in order to avoid audio feedback noise!

If you want, you can modify this code example a bit to get to know the two modules:

- Telephones in the early days could not transmitt fullband audio, but could only send 8000 samples a second. Try setting the sampling rate `rate` of the microphone and speaker to `8000` and listen to your own voice in narrowband!
- Audio transmission usually uses 2 bytes (also called 16-bit) to encode a single sample of audio data. Try setting the `sample_width` of the microphone and speaker to `1` (8-bit) and listen to the change in audio quality.
- Per default an incremental audio unit has 0.02 seconds (20 milliseconds) of audio, which results in short delay times and small increments. Try setting the `frame_length` of the microphone to a high value (> 1 second) and listen to the delay of your own voice.
- Try setting the sampling rate of the microphone to a different value than the sampling rate of the speaker. Try using values between `32000` and `48000`. What happens when the rate of the speaker is slower/higher?

```diff
- Changing these audio settings to extreme values might result in some unwanted loud sounds from your device.
```

---

[Next step: Working with an incremental speech recognition](02_incremental_asr.md)