# `os` is used to access files in a system-independent way.
import os

# Explanation of the Gtk, Adw, and GLib imports is in the `pyvizapp.py` file
# However, we are importing one extra library this time.
# GStreamer is a powerful media library, based on GObject.
# We use gstreamer as an easy way to invoke the GOOM visualizer
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gtk, Adw, Gst

# Hey it's the YouTube downloader again! See `pyvizapp.py` for more information.
from yt_dlp import YoutubeDL

# We run the download of the audio asynchronously 
import threading

# Like all the other pages, the GOOM page inherits from AdwNavigationPage
class PyVizGoomPage(Adw.NavigationPage):
    # Constructor function 
    def __init__(self, url, navigation_view):
        # Use the parent class's constructor logic.
        super().__init__()

        # Set the title of this page
        self.set_title("Visualizer Output")

        # Explanation for how these widgets work can be found in `pyvizapp.py`
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
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
        
        # Remove this page from the navigation view.
        navigation_view.pop()

        #Visualize the audio!
        self.viz()
        
        return
    
    # Helper function for GStreamer
    def on_eos(self, bus, message, loop):
        loop.quit()

    # Helper function for GStreamer
    def on_error(self, bus, message, loop):
        loop.quit()

    # The visualizer function.
    def viz(self):
        
        # Initialize GStreamer
        Gst.init(None)

        # The GStreamer media library is based on a "pipeline" approach.
        # Media is manipulated by putting it through various "elements".
        # Linking these elements together makes a "pipeline"
        # The following string defines our pipeline.
        # First, grab the audio we want to visualize from .\downloads\audio\cur_audio.wav.
        # Parse it using the "wavparse" element
        # Next, we branch out the pipeline using the "tee" element.
        # The first branch converts and resamples the audio into an optimal format,
        # then plays it using a platform-appropriate method.
        # Now, "t." lets us work on the second branch, which takes the parsed wav from just before the tee,
        # converts it to an appropriate format for visualization, visualizes it using GOOM,
        # and then converts and outputs the video feed in a platform-appropriate way.
        pipeline_str = "filesrc location=" + os.path.join("downloads", "audio", "cur_audio.wav") + " ! wavparse ! tee name=t ! queue ! audioconvert ! audioresample ! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink"
        
        # We parse and launch our pipeline with this convenience function.
        pipeline = Gst.parse_launch(pipeline_str)

        # This is basic GStreamer boilerplate to start the pipeline
        loop = GLib.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos, loop)
        bus.connect("message::error", self.on_error, loop)
        pipeline.set_state(Gst.State.PLAYING)

        # This allows the user to stop the playing from the terminal
        try:
            loop.run()
        except KeyboardInterrupt:
            pass

        # If we get here, the feed is over. Set the state from "playing" to "NULL"
        pipeline.set_state(Gst.State.NULL)

        return