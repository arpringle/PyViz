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
        welcome_text.set_label("Welcome to PyViz, the Python music visualizer.\nTo get started, enter a Youtube URL below, then hit 'Submit'!")
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
        url_entry_box.append(submit_button)

        # Append the completed url_entry_box to the mainbox
        mainbox.append(url_entry_box)

        # Create a box that will hold a label with "feedback text", as well as a spinner.
        feedback_text_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        feedback_text_box.set_halign(Gtk.Align.CENTER)

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

        # Connect the submit button's "clicked" signal to the submit button.
        submit_button.connect("clicked", self._submit_clicked, url_entry, feedback_text_spinner, feedback_text)

    # This is a callback function, activated whenever the user clicks "submit"
    def _submit_clicked(self, button, url_entry, spinner, feedback_text):

        # Grab the `url` function from the validators package,
        # and check it against the text in the URL entry.
        # If the function returns true, we can proceed.
        if validators.url(url_entry.get_text()):
            
            # If the URL is valid, write the value to a variable.
            # !Important! This is actually a list and not a string,
            # because the YoutubeDL object's "download" function
            # takes a list of URL's as its parameter.
            url = [url_entry.get_text()]

            # Create a new thread in which we can download from YouTube asycnronously.
            # We pass call the application object's "get_audio" function (defined below)
            # as the target of the thread.
            audioDlThread = threading.Thread(target=self.get_audio, args=(url, button, spinner, feedback_text))
            audioDlThread.start()
        
        # If the URL fails to validate, notify the user
        else: feedback_text.set_label("Content couldn't be fetched; invalid URL.");
    
    # This function downloads the data from YouTube. It is run asynchronously in a thread.
    def get_audio(self, url, submit_button, spinner, feedback_text):

        # We make some UI changes to indicate to the user that the program is working. 
        submit_button.set_sensitive(False)
        feedback_text.set_label("The program is fetching content from YouTube");
        spinner.start()

        # Declare a dictionary containing options for the downloader
        # TODO: Maybe expose some extra Download options to the user
        # ex - download video and use as background for visualization
        ydl_opts = {
            'format': 'wav/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        # Instantiate a `YoutubeDL` object, using `ydl_opts` as the parameter.
        # Then, call the `download` method, passing `url` as a parameter.
        # Finally, take the return value, and write it to a variable `error_code`.
        error_code = YoutubeDL(ydl_opts).download(url)
        submit_button.set_sensitive(True)
        feedback_text.set_label("");
        spinner.stop()



# THE REST OF THE PROGRAM LOGIC

# Instantiate the `PyVizApplication` object
app = PyVizApplication()

# Call the `run` method on the newly-created app.
# We also pass command line arguments to the `run` method via `sys.argv`
# We don't use command line arguments.
# However, gtk requires access to command-line arguments.
# Then, we save the exit status of the app to the variable `exit_status`
exit_status = app.run(sys.argv)

# After the app is done running, we exit the interpreter and raise the exit status via a method. 
sys.exit(exit_status)