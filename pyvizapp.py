# PACKAGE IMPORTS

# `os` is used to access files in a system-independent way.
import os

# GObject is a library for the C language that adds Object-Oriented features.
# `gi` (short for "GObject Introspection")is a package that provides Python bindings
# for the most popular GObject-based C libraries.
# Despite the underlying libraries inside the `gi` package being written in C, all of the code
# that they provide is still python code.
import gi

# From `gi`, we require the `gtk` library, version 4.0, as well as its dependency, GLib.
# `gtk` is a powerful cross-platform toolkit, originally written in C.
# Here we are using the Python language binding provided by `gi`
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

# `yt_dlp` is an incredibly powerful command-line tool for downloading content from YouTube.
# It also provides a Python package. Here, we import yt_dlp's 'YoutubeDL' class.
# This class provides the actual downloader function.
from yt_dlp import YoutubeDL

# We use the `validators` package to check that the URL that the user enters into the program
# is actually a valid URL before we do anything with it.
import validators

# Downloading a video is a long operation. By default, using YoutubeDL will freeze the GUI
# until the video is done downloading, making the user think something is broken.
# To do this, we perform the download operation asynchronously using this `threading` package.
import threading

import pyvizsearchresultspage

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
        window = Adw.ApplicationWindow(application=self, title="PyViz")
        # Restrict the window from getting too small
        window.set_size_request(600,600)

        navigation_view = Adw.NavigationView()

        splash_nav_page = Adw.NavigationPage()
        splash_nav_page.set_title("Welcome to PyViz")

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        header_bar.set_show_title(False)

        toolbar_view.add_top_bar(header_bar)

        # Create a box to hold the main content of the window. Allow it to grow.
        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=32)
        mainbox.set_vexpand(True)
        mainbox.set_hexpand(True)
        
        # Create an image from the logo file. Add it to the mainbox. 
        logo = Gtk.Image()
        logo.set_from_file(os.path.join("data","LOGO.png"))
        logo.set_size_request(128,256)
        logo.set_margin_top(32)
        mainbox.append(logo)

        # Create  greeting text, center it, add it to the mainbox
        welcome_text = Gtk.Label()
        welcome_text.set_justify(Gtk.Justification.CENTER)
        welcome_text.set_valign(Gtk.Align.CENTER)
        welcome_text.set_label("Welcome to PyViz, a Python music visualizer.\n\nStart by entering a YouTube search or URL into the box below.\nThen, hit 'Submit'.")
        mainbox.append(welcome_text)

        # Create a box that will hold the URL entry and the "Submit" button
        url_entry_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        url_entry_box.set_halign(Gtk.Align.CENTER)

        # Create the URL entry itself and add it to the url_entry_box
        url_entry = Gtk.Entry()
        url_entry.set_size_request(256, 0)
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

        toolbar_view.set_content(mainbox)

        splash_nav_page.set_child(toolbar_view)

        navigation_view.push(splash_nav_page)

        # Now that the mainbox is completed, add it as the child of the window. 
        window.set_content(navigation_view)

        # Present the window
        window.present()

        # Connect the submit button's "clicked" signal to the submit button.
        submit_button.connect("clicked", self._submit_clicked, url_entry, feedback_text_spinner, feedback_text, navigation_view)

    # This is a callback function, activated whenever the user clicks "submit"
    def _submit_clicked(self, button, url_entry, spinner, feedback_text, navigation_view):
            
        # If the URL is valid, write the value to a variable.
        # !Important! This is actually a list and not a string,
        # because the YoutubeDL object's "download" function
        # takes a list of URL's as its parameter.
        url = [url_entry.get_text()]

        # Create a new thread in which we can download from YouTube asycnronously.
        # We pass call the application object's "get_audio" function (defined below)
        # as the target of the thread.
        audioDlThread = threading.Thread(target=self.get_audio, args=(url, button, spinner, feedback_text, navigation_view))
        audioDlThread.start()
    
    # This function downloads the data from YouTube. It is run asynchronously in a thread.
    def get_audio(self, url, submit_button, spinner, feedback_text, navigation_view):

        # We make some UI changes to indicate to the user that the program is working.
        # Namely, make the submit button insensitive and change the feedback text.
        # Also, show a spinner.
        submit_button.set_sensitive(False)
        feedback_text.set_label("The program is fetching content from YouTube");
        spinner.start()

        try:
            # Declare a dictionary containing options for the downloader
            # TODO: Maybe expose some extra Download options to the user
            # ex - download video and use as background for visualization
            ydl_opts = {
                'format': 'wav/bestaudio/best',
                'paths': {'home' : os.path.join("downloads", "audio")},
                'outtmpl' : "cur_audio",
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
            }

            # Instantiate a `YoutubeDL` object, using `ydl_opts` as the parameter.
            # Then, call the `download` method, passing `url` as a parameter.
            # Finally, take the return value, and write it to a variable `error_code`.
            error_code = YoutubeDL(ydl_opts).download(url)
            # After YoutubeDL finishes downloading, 
            feedback_text.set_label("")
            submit_button.set_sensitive(True)
            spinner.stop()
            self.visualize_audio()
        
        except:

            if validators.url(url[0]):
                feedback_text.set_label("The program was unable to parse the URL.")
                submit_button.set_sensitive(True)
                spinner.stop()

            else:
                navigation_view.push(pyvizsearchresultspage.PyVizSearchResultsPage(feedback_text, submit_button, spinner, url, navigation_view))
                
            

    def visualize_audio(self):
        print("TODO")