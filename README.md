# PyViz

PyViz is a Python-based music visualizer.

It allows you to make a music visualization from your favorite song or YouTube video quickly and easily.

## Windows Run Instructions

NOTE: For any command, do not paste the tick marks (`) in with the command, just what's between them.

Running the program gets a bit... complicated, but it's doable.

Had I known the complications, I might not have chosen GTK, as it adds most of the complexity.

That being said...

To run PyViz you must...

0) Download and unzip the PyVizSourceCode folder.

1) Download the MSYS2 installer from [this link.](https://github.com/msys2/msys2-installer/releases/download/2024-01-13/msys2-x86_64-20240113.exe) MSYS2 is a UNIX environment for Windows, and it provides all of the dependencies that PyViz needs in order to run. Install MSYS2 with default options, and, when the installer is finished, uncheck the box to start MSYS2. We do not want to launch that now.

2) MSYS2 will be installed into the directory `C:\msys64`. Using file explorer, copy the entire unzipped PyVizSourceCode into the folder `C:\msys64\home\<your-username-here>\`.

3) Next, search in the start menu for `ucrt64` and run it.

4) A terminal will pop up, copy and paste the following very long command: `pacman -Syu --noconfirm ; pacman -S --noconfirm mingw-w64-ucrt-x86_64-gtk4 mingw-w64-ucrt-x86_64-python3 mingw-w64-ucrt-x86_64-python3-gobject mingw-w64-ucrt-x86_64-gstreamer mingw-w64-ucrt-x86_64-gst-plugins-base mingw-w64-ucrt-x86_64-gst-plugins-good mingw-w64-ucrt-x86_64-gst-plugins-bad mingw-w64-ucrt-x86_64-gst-plugins-ugly mingw-w64-ucrt-x86_64-yt-dlp mingw-w64-ucrt-x86_64-ffmpeg mingw-w64-ucrt-x86_64-python-pygame mingw-w64-ucrt-x86_64-python-numpy mingw-w64-ucrt-x86_64-python-pip mingw-w64-ucrt-x86_64-libadwaita mingw-w64-ucrt-x86_64-python-librosa ; pip install validators`

(yes, that is a one-line command.)

This command installs all needed dependencies.

If prompted for input during step 4, press "Y" followed by "enter".
You may have also have ucrt64 close on you. If this happens, simply reopen the terminal and try the command again.

5) Once that very long command is done running, you can run `python /PyVizSourceCode/main.py` to run PyViz.

That's a lot to do, but, after the initial setup, you'll never have to do it again. Any time you want to run PyViz, simply open `ucrt64` from the start menu and enter `python /PyVizSourceCode/main.py`