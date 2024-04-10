# PyViz, a Python music visualizer.
# Program by Austin Pringle, Caleb Rachocki, & Caleb Ruby
# Pennsylvania Western University, California


# PACKAGE IMPORTS

# `sys` is used to grab command-line args and return application status.
# (We don't support command-line args, but the widget toolkit does, so that's why we need it)
import sys

# GObject is a library for the C language that adds Object-Oriented features.
# `gi` is a package that provides Python bindings for the most popular GObject-based C libraries.
# Despite the underlying libraries inside the `gi`` package being written in C, all of the code
# that they provide is still python code.
import gi

# From `gi`, we require the `gtk` library, version 4.0, as well as its dependency, GLib.
# `gtk` is a powerful cross-platform toolkit, originally written in C.
# Here we are using the Python language binding provided by `gi``
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

# `yt_dlp` is an incredibly powerful command-line tool for downloading content from YouTube.
# It also provides a Python package. Here, we import yt_dlp's 'YoutubeDL' class.
# This class provides the actual downloader function.
from yt_dlp import YoutubeDL

# We use the `validators` package to check that the URL that the user enters into the program
# is actually a valid URL before we do anything with it.
import validators

# Downloading a video is a long operation. By default, using YoutubeDL will freeze the GUI
# until the video is done downloading, making the user think something is broken
# To do this, we perform the download operation asynchronously using this `threading` package.
import threading


# THE APPLICATION CLASS

# Create the Application Class, inheriting from GtkApplication
class PyVizApplication (Gtk.Application):

    # Initialization boilerplate 
    def __init__(self):
        super().__init__(application_id="edu.pennwest.PyViz")
        GLib.set_application_name("PyViz")

    # On activation of the application, this function is called.
    def do_activate(self):
        # Create a new GtkWindow, tied to the application. 
        window = Gtk.ApplicationWindow(application=self, title="PyViz")
        # Restrict the window from getting too small
        window.set_size_request(600,600)

        # Create a box to hold the main content of the window. Allow it to grow.
        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        mainbox.set_vexpand(True)
        mainbox.set_hexpand(True)
        
        # Create an image from the logo file. Add it to the mainbox. 
        logo = Gtk.Image()
        logo.set_from_file("./data/LOGO.png")
        logo.set_size_request(128,256)
        mainbox.append(logo)

        # Create  greeting text, center it, add it to the mainbox
        welcome_text = Gtk.Label()
        welcome_text.set_justify(Gtk.Justification.CENTER)
        welcome_text.set_valign(Gtk.Align.CENTER)
        welcome_text.set_label("Welcome to PyViz, the Python music visualizer.\n\nTo get started, enter a Youtube URL below, then hit 'Submit'!")
        mainbox.append(welcome_text)

        # Create a box that will hold the URL entry and the "Submit" button
        url_entry_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        url_entry_box.set_halign(Gtk.Align.CENTER)

        # Create the URL entry itself and add it to the url_entry_box
        url_entry = Gtk.Entry()
        url_entry.set_text("Enter URL Here...")
        url_entry_box.append(url_entry)

        # Create the submit button and add it to the url_entry_box
        submit_button = Gtk.Button()
        submit_button.set_label("Submit")
        submit_button.connect("clicked", self._submit_clicked, url_entry)
        url_entry_box.append(submit_button)

        # Append the completed url_entry_box to the mainbox
        mainbox.append(url_entry_box)

        # Create a box that will hold a label with "feedback text", as well as a spinner.
        feedback_text_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        url_entry_box.set_halign(Gtk.Align.CENTER)

        # Create a label to hold the feedback text, ie, any errors or messages.
        # Then add it to the feedback_text_box
        feedback_text = Gtk.Label()
        feedback_text_box.append(feedback_text)

        # Create a loading spinner to show beside the feedback_text if an operation is taking place.
        # Then add it to the feedback_text_box.
        feedback_text_spinner = Gtk.Spinner()
        feedback_text_box.append(feedback_text_spinner)

        # Add the feedback_text_box to the mainbox
        mainbox.append(feedback_text_box)

        # Now that the mainbox is completed, add it as the child of the window. 
        window.set_child(mainbox)

        # Present the window
        window.present()

    # This is a callback function, activated whenever the user clicks "submit"
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
                }
        
        error_code = YoutubeDL(ydl_opts).download(url)

app = PyVizApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)