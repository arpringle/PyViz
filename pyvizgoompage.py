import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gtk, Adw, Gst

from yt_dlp import YoutubeDL

import threading

class PyVizGoomPage(Adw.NavigationPage):
    def __init__(self, url, navigation_view):
        super().__init__()
        self.set_title("Visualizer Output")

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 16)
        mainbox.set_valign(Gtk.Align.CENTER)
        
        spinner = Gtk.Spinner()
        spinner.set_size_request(64,64)
        spinner.set_vexpand(True)

        spinner.start()
        mainbox.append(spinner)

        loading_text = Gtk.Label()
        loading_text.set_label("\nPlease wait...\n\nYour song is being downloaded.")
        loading_text.set_justify(Gtk.Justification.CENTER)
        loading_text.add_css_class("title-1")
        mainbox.append(loading_text)

        explain_text = Gtk.Label()
        explain_text.set_label("Your visualizer will start in its own window, momentarily.")
        explain_text.set_justify(Gtk.Justification.CENTER)
        mainbox.append(explain_text)

        toolbar_view.set_content(mainbox)

        self.set_child(toolbar_view)

        download_thread = threading.Thread(target=self.download, args=(url, navigation_view))
        download_thread.start()

    def download(self, url, navigation_view):
        ydl_opts = {
            'format': 'wav/bestaudio/best',
            'paths': {'home' : os.path.join("downloads", "audio")},
            'outtmpl' : "cur_audio",
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }
        YoutubeDL(ydl_opts).download(url)

        navigation_view.pop()
        self.viz()
        return

    def on_eos(self, bus, message, loop):
        loop.quit()

    def on_error(self, bus, message, loop):
        loop.quit()

    def viz(self):
        Gst.init(None)

        pipeline_str = "filesrc location=" + os.path.join("downloads", "audio", "cur_audio.wav") + " ! wavparse ! tee name=t ! queue ! audioconvert ! audioresample ! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink"
        pipeline = Gst.parse_launch(pipeline_str)

        loop = GLib.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self.on_eos, loop)
        bus.connect("message::error", self.on_error, loop)

        
        pipeline.set_state(Gst.State.PLAYING)

        try:
            loop.run()
        except KeyboardInterrupt:
            pass

        pipeline.set_state(Gst.State.NULL)

        return