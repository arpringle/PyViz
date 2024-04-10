import sys

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

from yt_dlp import YoutubeDL

import validators

import threading

class PyVizApplication (Gtk.Application):

    def __init__(self):
        super().__init__(application_id="edu.pennwest.PyViz")
        GLib.set_application_name("PyViz")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="PyViz")
        window.set_size_request(600,600)

        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        mainbox.set_vexpand(True)
        mainbox.set_hexpand(True)
        
        logo = Gtk.Image()
        logo.set_from_file("~/data/LOGO.png")
        logo.set_size_request(128,256)
        mainbox.append(logo)

        welcome_text = Gtk.Label()
        welcome_text.set_justify(Gtk.Justification.CENTER)
        welcome_text.set_valign(Gtk.Align.CENTER)
        welcome_text.set_label("Welcome to PyViz, the Python music visualizer.\n\nTo get started, enter a Youtube URL below, then hit 'Submit'!")
        mainbox.append(welcome_text)

        url_entry_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        url_entry_box.set_halign(Gtk.Align.CENTER)

        url_entry = Gtk.Entry()
        url_entry.set_text("hello")
        url_entry_box.append(url_entry)

        submit_button = Gtk.Button()
        submit_button.set_label("Submit")
        submit_button.connect("clicked", self._submit_clicked, url_entry)
        url_entry_box.append(submit_button)

        mainbox.append(url_entry_box)

        window.set_child(mainbox)
        window.present()

    def _submit_clicked(self, button, user_data):
        if validators.url(user_data.get_text()) == True:
            url = [user_data.get_text()]
            audioDlThread = threading.Thread(target=self.get_audio, args=(url, button))
            audioDlThread.start()
                
        else: print("err: invalid URL")
    
    def get_audio(self, url, submit_button):
        submit_button.set_sensitive(False)
        ydl_opts = {
                'format': 'mp3/bestaudio/best',
                'path' : '~/dls',
                }
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

app = PyVizApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)