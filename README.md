# PyViz

PyViz is a Python-based music visualizer.

It allows you to make a music visualization from your favorite song or YouTube video quickly and easily.

## Run Instructions

### Windows

On Windows we recommend downloading our dedicated installer. It takes some time for it to do its thing (potentially a really long time), however, it should configure all of the needed dependencies automatically.

You can find the installer download here: [TODO]

### Linux

#### Dependencies

Running PyViz on Linux requires a few packages.

On Debian and related distributions (Ubuntu, Mint, Pop!_OS, etc), open a terminal and enter:

`sudo apt install python3 python3-gi python3-validators yt-dlp libadwaita-1-0 libgstreamer1.0-0`

> Please note: Debian Stable does not contain the correct versions for all of these dependencies. The program will likely not run on Debian stable, but it should work on Debian Testing.

On Fedora and related distributions (Red Hat, Rocky, etc):

`sudo dnf install python3 python3-gobject python3-validators yt-dlp libadwaita libgstreamer1`

#### Next Steps

Once you have the dependencies installed, simply download the repository from GitHub by pressing the "Code" button and then the "Download Zip" Button. Once you have it downloaded, open a terminal and enter the following commands in order:

```
cd ~/Downloads
unzip PyViz-Main.zip
cd PyViz-Main
python3 main.py
```