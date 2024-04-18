import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gtk, Adw, Gst

from yt_dlp import YoutubeDL

import threading

class PyVizGoomPage(Adw.NavigationPage):
    def __init__(self, url_file_path):
        super().__init__()
        self.set_title("Visualizer Output")

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
        
        spinner = Gtk.Spinner()
        spinner.set_size_request(64,64)
        spinner.set_vexpand(True)
        spinner.set_valign(Gtk.Align.CENTER)
        spinner.start()
        mainbox.append(spinner)

        toolbar_view.set_content(mainbox)

        self.set_child(toolbar_view)

        download_thread = threading.Thread(target=self.download, args=(url_file_path, spinner, mainbox))
        download_thread.start()

    def download(self, url_file_path, spinner, mainbox):
        ydl_opts = {
            'format': 'wav/bestaudio/best',
            'paths': {'home' : os.path.join("downloads", "audio")},
            'outtmpl' : "cur_audio",
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }
        url=""
        for line in open(url_file_path, "r"):
            if line != "URL\n":
                url = line[4:(len(line)-1)]
        YoutubeDL(ydl_opts).download(url)
        self.viz(spinner, mainbox)
        return

    def on_eos(self, bus, message, loop):
        print("End of stream")
        loop.quit()

    def on_error(self, bus, message, loop):
        print("Error:", message.parse_error())
        loop.quit()

    def viz(self, spinner, mainbox):
        Gst.init(None)

        pipeline_str = "filesrc location=" + os.path.join("downloads", "audio", "cur_audio.wav") + " ! decodebin ! tee name=t ! queue ! audioconvert ! audioresample ! autoaudiosink t. ! queue ! audioconvert ! goom ! videoconvert ! autovideosink"
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