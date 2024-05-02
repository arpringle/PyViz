# PyViz, a Python music visualizer.
# Program by Austin Pringle, Caleb Rachocki, & Caleb Ruby
# Pennsylvania Western University, California
#
# pyvizvispage.py
# This file contains the loading page for our custom visualizer.
# This page has the logic to download the song and create our custom visualization

# `os` is used to access files in a system-independent way.
import os

# Explanation of these imports is in the `pyvizapp.py` file
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

# Hey it's the YouTube downloader again! See `pyvizapp.py` for more information.
from yt_dlp import YoutubeDL

# We run the download of the audio asynchronously 
import threading

import visualizerengine

# Like all the other pages, the vis page inherits from AdwNavigationPage
class PyVizVisPage(Adw.NavigationPage):
    # Constructor function 
    def __init__(self, url, navigation_view, fg_color, bg_color):
        # Use the parent class's constructor logic.
        super().__init__()



        self.fg_color = fg_color
        self.bg_color = bg_color

        # Set the title of this page
        self.set_title("Visualizer Output")

        # Explanation for how these widgets work can be found in `pyvizapp.py`
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        header_bar.set_show_back_button(False)
        toolbar_view.add_top_bar(header_bar)

        # Create a vertical box to hold the main content of this page.
        # Space its children out by 16 px. Vertically center it.
        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 16)
        mainbox.set_valign(Gtk.Align.CENTER)
        
        # A spinner  to show while the video is downloading.
        spinner = Gtk.Spinner()
        spinner.set_size_request(64,64)
        spinner.set_vexpand(True)
        spinner.start()
        mainbox.append(spinner)

        # 2 blocks of text to explain what is happening behind the screen...

        # ...a big "downloading message"
        loading_text = Gtk.Label()
        loading_text.set_label("\nPlease wait...\n\nYour song is being downloaded.")
        loading_text.set_justify(Gtk.Justification.CENTER)
        loading_text.add_css_class("title-1")
        mainbox.append(loading_text)

        # ...a message explaining that the visualizer is to pop out in its own window.
        explain_text = Gtk.Label()
        explain_text.set_label("Your visualizer will start in its own window, momentarily.")
        explain_text.set_justify(Gtk.Justification.CENTER)
        mainbox.append(explain_text)

        # Set the mainbox as the content widget of the toolbar view
        toolbar_view.set_content(mainbox)

        # Set the toolbar view as the child of the nav page
        self.set_child(toolbar_view)

        # Start the thread to download the video.
        download_thread = threading.Thread(target=self.download, args=(url, navigation_view))
        download_thread.start()

    def download(self, url, navigation_view):
        
        # Downloader options dictionary
        ydl_opts = {
            # Ask youtube to output a high-quality .wav file
            'format': 'wav/bestaudio/best',

            # Output the file to a local folder called "downloads\audio"
            'paths': {'home' : os.path.join("downloads", "audio")},

            # Name the file cur_audio.wav
            'outtmpl' : "cur_audio",

            # Sometimes YouTube fails to properly give us the file we asked for.
            # Just to be safe, we attempt to convert the output to .wav
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        # Download the audio in question
        YoutubeDL(ydl_opts).download(url)
        
        # Remove this page from the navigation view when the loading is complete.
        navigation_view.pop()

        #Visualize the audio!
        self.viz()
        
        return

    def viz(self):
        visualizerengine.run_audio_visualizer(os.path.join("downloads","audio","cur_audio.wav"), self.fg_color, self.bg_color) 