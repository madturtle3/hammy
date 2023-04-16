# What is Hammy?
`Hammy` is a morse code turned ASK that you can use for radios... or anything, really. My lack of documentation
Has led to a problematic lack of understanding the code, so mantenance or improvement without completely starting again with a new project is unlikely.

# Installation
The requirements.txt has the packages necessary for installation, however, the `python3 dev` and `portaudio dev`
(exact naming will vary by system) must be installed prior to installation. However, after the installation,
feel free to remove the packages. (this is not necessary on windows as far as I am aware.)
Here are the installations necessary for different computers:
## Macos
```bash
python3 -m venv venv/
source venv/bin/activate
brew install portaudio
pip install -r requirements.txt
deactivate
```
NOTE: On macos, unfortunately, there will be a remnant package (portaudio) that will stay on your system.
This is the price you pay for using pyaudio.
## Fedora
```bash
python3 -m venv venv/
yes | sudo dnf install python-devel portaudio-devel
pip install -r requirements.txt
```
If you don't want python-devel and portaudio-devel on your system, use this to remove it:
```bash
yes | sudo dnf remove python-devel portaudio-devel
```

## Windows
```
pip install -r requirements.txt
```
Unfair that this one is the easiest.