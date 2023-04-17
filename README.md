# About
Uses Autohotkey v2 to keep track of what is happening during an audio recording, uses Python to split that recording into parts with the labels you made.

Built on Windows. May work on other systems.

# How to use
### Requirements
Install [Python](https://www.python.org/downloads/) and [Autohotkey v2](https://www.autohotkey.com/v2/)
`pip install audioread`
All other modules used are included with python.

**Your audio files MUST be of the format yyyymmddhhmmss.wav/mp3/ogg etc**

14-character, 24-hour datetime

If you need to convert your filenames, perhaps just modify the part of the python file where I already do that.

### Setup
Modify initial python variables to your needs.

I suggest pasting an alias of the ahk script in your Windows startup folder so that you're always ready to go. (Press Win+R then type "shell:startup")

### Usage
Once timestampAndLabel.ahk is running:

    Press Ctrl+Shift+Alt+t to initialize recording.

    Press Ctrl+Shift+Alt+t again to indicate the end of a section and describe what happened.

    Press Ctrl+Shift+Alt+n to restart script and prime for a new recording.

Once your audio files have been moved to the audio-labelling folder

    Simply run divideByLabel.py

