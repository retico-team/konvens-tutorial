# Installing retico

Retico is a python library that requires Python version 3.10. You can check which version of Python you have installed by running the following command:

```bash
python3 --version
```

This will show you which version of Python is installed. Any version above Python 3.10 will be fine.

## Dependencies

To install retico, some dependencies need to be installed first. Retico relies mainly on python libraries that will be automatically installed when installing retico. Two external libraries need to be installed beforehand: A library called *PortAudio* which is used to record and handle various different audio streams, and a library called *ffmpeg*, which is used to convert between many different audio formats.

The way they have to be installed depends on the operating system you are using.

### Linux

The package managers on most Linux distributions will have *PortAudio* and *ffmpeg* in their repositories.

For apt-based distributions, use the following command:

```bash
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
```

For other distributions, you most likely have to search for ways to install *PortAudio* and *ffmpeg* or build these dependencies yourself.

### MacOS

On MacOS, you will need a package manager to install *PortAudio* and *ffmpeg*. This might either be [Homebrew](https://brew.sh/) or [MacPorts](https://macports.org/).

With Homebrew, you can install these dependencies with the following command:

```bash
brew install portaudio ffmpeg
```

With MacPorts, you have to use the following command:

```bash
sudo port install portaudio ffmpeg
```

### Windows

Under Windows, *PortAudio* is automatically installed as a dependency. *ffmpeg* needs to be installed from their [website](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z), and the binaries have to be added to that PATH variable.

An installation tutorial for Windows can be found [here](https://cran.r-project.org/web/packages/act/vignettes/installation-ffmpeg.html).

## Installing Retico

To install retico, use the Python package manager `pip` to install the framework and all its dependencies:

```bash
pip3 install --upgrade retico
```

## Check if it worked

To test if your retico installation was successful, try importing the retico library and printing out the version in Python:

```python
import retico
print(retico.__version__)
```

---

[Next Step: Creating a simple echo network](01_simple_echo.md)