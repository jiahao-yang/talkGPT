#!/bin/bash

python -m venv venv
#This is for Linux . venv/bin/activate
This is for Windows . venv/Scripts/activate

# MacOS only
# brew install portaudio
# brew install flac
# brew install ffmpeg

# Linux only
sudo apt-get install portaudio19-dev
sudo apt-get install flac
sudo apt-get install ffmpeg
sudo apt-get install espeak

pip install -r ./requirements.txt
