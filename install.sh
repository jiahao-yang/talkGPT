#!/bin/bash

python -m venv venv
. venv/bin/activate

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
