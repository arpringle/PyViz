# PACKAGE IMPORTS

# `os` is used to access files in a system-independent way.
import os

# GObject is a library for the C language that adds Object-Oriented features.
# `gi` (short for "GObject Introspection") is a package that provides Python versions
# of the most popular GObject-based C libraries.
# Despite the underlying libraries inside the `gi` package being written in C, all of the code
# that they provide is still python code.
import gi

# From `gi`, we require the`Gtk`, and `Adw` libraries,
# and make sure to get the latest major versions.
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

# Then, we officially import what we need from `gi`.
# As for what these packages actually do:
#
# - `GLib` is an alternative standard library for C, written with GObject in mind.
#   It implements many common data structures and similar things.
#   The package imported here is the Python version of GLib.
#   We don't directly use it, but our next two libraries depend on it heavily.  
# 
# - `Gtk` is a powerful cross-platform GUI toolkit, originally written in C.
#   Here, we use the Python version as the basis for our GUI.
#
# - `Adw` is the Python version of a C library called "libadwaita".
#   libadwaita extends the Gtk library with a few fancy new widgets.
from gi.repository import GLib, Gtk, Adw

# `yt_dlp` is an incredibly useful command-line tool for downloading content from YouTube.
# `yt-dlp` also provides a Python package. Here, we import yt_dlp's 'YoutubeDL' class.
# This class provides the actual downloader function.
from yt_dlp import YoutubeDL

# We use the `validators` package to check that the URL that the user enters into the program
# is actually a valid URL.
import validators

# Downloading a video is a long operation. By default, using YoutubeDL will freeze the GUI
# until the video is done downloading, making the user think something is broken.
# To do this, we perform the download operation asynchronously using this `threading` package.
import threading

# This lets us nuke a directory and all of its contents.
# Used to give us a fresh .tmp directory ever time.
from shutil import rmtree

# These pages pop up on the navigation depending on what the user does.
# More explanation in their own files.
import pyvizsearchresultspage
import pyvizcustomizerpage

# THE APPLICATION CLASS

# Create the Application Class, inheriting from AdwApplication
# 
# The AdwApplication class handles a lot of the initialization
# that Gtk and Adw need in order to run properly.
class PyVizApplication (Adw.Application):

    # Constructor function 
    def __init__(self):

        # Use the constructor from the parent class.
        # AdwApplication requires a unique app identifier.
        # This is typically done via a domain-based identifier like the below
        super().__init__(application_id="edu.pennwest.PyViz")

        # Set the user-facing application name as "PyViz"
        GLib.set_application_name("PyViz")

    # On activation of the application, this function is automatically called.
    # We build the UI on activation of the application.
    def do_activate(self):

        # Create a new AdwApplicationWindow to hold the UI.
        window = Adw.ApplicationWindow(application=self, title="PyViz")

        # Restrict the window from getting too small
        window.set_size_request(600,600)

        # The AdwNavigationView widget allows for a page-based layout.
        # This is useful because we can present options in pages.
        # It contains a stack of AdwNavigationPage widgets.
        navigation_view = Adw.NavigationView()

        # We create the first AdwNavigationPage, which holds the initial splash screen.
        # We set the title of the page, as well.
        splash_nav_page = Adw.NavigationPage()
        splash_nav_page.set_title("Welcome to PyViz")

        # AdwToolbarView is a widget that has 3 types of children:
        # - A singular "content" widget
        # - Any number of "top bar" children
        # - Any number of "bottom bar" children.
        #
        # This widget is meant to manage the main view:
        # - The "content" widget is the actual page contents.
        # - The top and bottom bars are toolbars attached to the top/bottom of the window.
        toolbar_view = Adw.ToolbarView()

        # To allow for more customization,the AdwApplicationWindow does not have a
        # "window handle" by default. (The part at the top that lets you move the window).
        # To account for this, we create an AdwHeaderBar (Adw's version of a window handle),
        # and add it to the toolbar_view as a top bar
        header_bar = Adw.HeaderBar()
        header_bar.set_show_title(False)
        toolbar_view.add_top_bar(header_bar)

        # Create a vertical box to hold the main content of this page.
        # Space its children out by 32 px.
        # Allow it to grow.
        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=32)
        mainbox.set_vexpand(True)
        mainbox.set_hexpand(True)
        
        # Create an image from the logo file, set its size, space it out from the top.
        # Finally, add it to the mainbox.
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

        # Create a horizontal sub-box that will hold the URL entry and the "Submit" button.
        url_entry_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        url_entry_box.set_halign(Gtk.Align.CENTER)

        # Create the URL entry and add it to the url_entry_box
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

        # Create another horizontal sub-box that will hold...
        # - A label with "feedback text"
        # - A spinner to show when the program is loading.
        feedback_text_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=8)
        feedback_text_box.set_halign(Gtk.Align.CENTER)

        # Create a label to hold the feedback text, ie, any errors or messages.
        # Then add it to the feedback_text_box.
        feedback_text = Gtk.Label()
        feedback_text_box.append(feedback_text)

        # Create a loading spinner to show beside the feedback_text.
        # This is used when an operation is taking place.
        # The spinner is hidden by default, only shown when we call the `.start()` method.
        # Then we, add it to the feedback_text_box.
        feedback_text_spinner = Gtk.Spinner()
        feedback_text_box.append(feedback_text_spinner)

        # Add the feedback_text_box to the mainbox
        mainbox.append(feedback_text_box)

        # Now that we have added everything we need to the mainbox,
        # We set it as the main content widget of the toolbar_view
        toolbar_view.set_content(mainbox)

        # Now that the toolbar_view has been given both a Window handle and content,
        # we set it as the singular child of the navigation page.
        splash_nav_page.set_child(toolbar_view)

        # Push the completed splash page into the navigation 
        navigation_view.push(splash_nav_page)

        # Now that the navigation view has at least one page,
        # we can add it as the child of the window. 
        window.set_content(navigation_view)

        # Present the window
        window.present()

        # Connect the submit button's "clicked" signal to the appropriate function.
        #This means that the `_submit_clicked` method will be called
        # whenever the submit button is clicked
        #
        # The reason we pass so many UI elements as parameters is because
        # we want to modify those particular elements when the submit button is clicked,
        # in order to indicate to the user that something is happening.
        submit_button.connect("clicked", self._submit_clicked, url_entry, feedback_text_spinner, feedback_text, navigation_view)

    # This is a callback function, activated whenever the user clicks "submit".
    def _submit_clicked(self, button, url_entry, spinner, feedback_text, navigation_view):
            
        # Get the text from the URL entry, and write it to the variable `url`
        # !Important! Please note that the URL variable is actually a list and not a string.
        # because the YoutubeDL object's "download" function takes a list of URLs
        # as its parameter. However, we do not use that functionality.
        url = [url_entry.get_text()]

        # Create a new thread in which we can download from YouTube asycnronously.
        # We pass the Application object's "get_audio" method (defined below)
        # as the target of the thread.
        # Also, we further pass along all of the UI elements we wish to change.
        audioDlThread = threading.Thread(target=self.get_audio, args=(url, button, spinner, feedback_text, navigation_view))
        audioDlThread.start()
    
    # This function downloads the data from YouTube. It is run asynchronously in a thread.
    def get_audio(self, url, submit_button, spinner, feedback_text, navigation_view):

        # We make some UI changes to indicate to the user that the program is working.
        # Namely, make the submit button insensitive to input and change the feedback text.
        # Also, show the spinner.
        submit_button.set_sensitive(False)
        feedback_text.set_label("The program is fetching content from YouTube");
        spinner.start()

        # We don't download the actual audio now. That comes later.
        # Instead, we just want metadata about the video,
        # in order to show  the user what result we came back with for their query.
        # However, how do we tell if the input is a URL or a search?
        # Here, we `try` to treat it as a URL before anything else:
        try:
            
            # This is weird, but basically, nuke the .tmp directory,
            # Then, if we get any error, just create it instead.
            # Technically, we don't need to create the .tmp directory here,
            # because the YouTube downloader does it automatically, but this block
            # basically does all the error handling.
            try: rmtree(".tmp")
            except: os.mkdir(".tmp")

            # This is a dictionary containing runtime options for the downloader.
            ydl_search_opts = {
                # Save the downloaded data to a directory called .tmp\1\
                'paths': {'home' : os.path.join(".tmp", 1)},

                # Don't actually download the video itself at all.
                # Remember, right now, we just want metadata.
                'skip_download' : 'true',

                # Write the thumbnail to file
                'writethumbnail' : 'true',

                # Write the YouTube URL to file
                'writeurllink' : 'true',

                # If it's the thumbnail, we name the output file something like
                # "IMG-videotitle.fileextension"
                # If not, don't use the `IMG` part
                'outtmpl' : {
                    'default' : '%(title)s.%(ext)s',
                    'thumbnail' : 'IMG-%(title)s'
                }
                
            }

            # Instantiate a `YoutubeDL` object, using `ydl_opts` as the parameter.
            # Then, call the `download` method, passing `url` as a parameter.
            # This treats all user entries as URLs.
            # If YoutubeDL throws an error, the flow won't continue past this statement.
            YoutubeDL(ydl_opts).download(url)

            # If we get here, it means that the download was successful.
            # After YoutubeDL finishes, we revert the UI changes on the splash page:
            feedback_text.set_label("")
            submit_button.set_sensitive(True)
            spinner.stop()

            # Now that we know which video we want, we can continue.
            # Push the visualizer customizer page to the navigation stack.
            navigation_view.push(pyvizcustomizerpage.PyVizCustomizerPage())
        
        # If the download threw an error, we end up down here.
        except:
            # We check if the user input is a URL at all, using the `validators` package.
            if validators.url(url[0]):
                # If it is a URL, we tell the user that the URL was unable to parse.
                feedback_text.set_label("The program was unable to parse the URL.")

                # Make the submit button sensitive again, and stop the spinner.
                # However, do not hide the feedback text
                submit_button.set_sensitive(True)
                spinner.stop()

            # However, if we get down here, it means that both...
            # 1) The download failed
            # 2) The entry doesn't validate as a URL
            # ...then we can treat the entry as a search query instead.
            else:
                # We create the search results page, passing...
                # 1) the UI elements we want to change
                # 2) The user input
                # ...as parameters to the constructor.
                # After it is created, it is pushed to the navigation view. 
                navigation_view.push(pyvizsearchresultspage.PyVizSearchResultsPage(url, feedback_text, submit_button, spinner, navigation_view))