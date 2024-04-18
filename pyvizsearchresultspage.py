# `os` is used to access files in a system-independent way.
import os

# Explanation of these imports is in the `pyvizapp.py` file
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

# We do a long-running YouTube search operation on this page, so we run it asynchronously.
import threading

# Hey it's the YouTube downloader again! See `pyvizapp.py` for more information.
from yt_dlp import YoutubeDL

# This lets us nuke a directory and all of its contents.
# Used to give us a fresh .tmp directory ever time.
from shutil import rmtree

from PIL import Image

# Once the user selects the search result they want, we need to open this page.
# It's the page that lets the user customize the visualizer.
import pyvizcustomizerpage

# Inherit from AdNavigationPage.
class PyVizSearchResultsPage(Adw.NavigationPage):

    # Constructor function.
    # In the constructor, we pass some of the UI elements from the last page.
    # This is so we can return them to their default state.
    def __init__(self, search_query, feedback_text, submit_button, spinner, navigation_view):
        
        # Use the parent class's constructor logic.
        super().__init__()

        # Set the title of this page
        self.set_title("Search Results")

        # Return UI elements on the splash page to their default state.
        feedback_text.set_label("")
        submit_button.set_sensitive(True)
        spinner.stop()

        # Explanation for how these widgets work can be found in `pyvizapp.py`
        toolbar_view = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        # GtkScrolledWindow allows us to scroll the content when it becomes too big.
        # The second line specifies that we only want to scroll vertically,
        # and never horizontally.
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Create a vertical box to hold the main content of this page.
        # Space its children out by 8 px.
        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)

        # The resultsbox is one of the two child widgets of mainbox.
        # It holds the search results.
        resultsbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)

        # Add the resultsbox to the mainbox
        mainbox.append(resultsbox)

        # The search page gets shown before the search is done happening.
        # Therefore, the page would be empty by default.
        # To show the user that we are working, we show a 32px x 32px spinner.
        # It goes under the resultsbox, so you can still see that the program is working
        # As the various search results start to load in.
        search_spinner = Gtk.Spinner()
        search_spinner.set_margin_top(16)
        search_spinner.set_size_request(32,32)
        mainbox.append(search_spinner)
        search_spinner.start()

        # Set the mainbox as the child of the scrolled window to make it scrollable.
        scrolled_window.set_child(mainbox)

        # Set the scrolled window as the main content of the toolbar view.
        toolbar_view.set_content(scrolled_window)

        # Set the completed toolbar_view as the child of this page.
        self.set_child(toolbar_view)

        # Create a new thread in which we can search YouTube.
        # The target of the thread is the searchYoutube method.
        # We pass the search query, as well as a few relevant UI elements, as parameters.
        searchThread = threading.Thread(target=self.searchYouTube, args=(search_query, resultsbox, search_spinner, navigation_view))
        searchThread.start()
    
    # This function actually does the YouTube searching.
    def searchYouTube(self, search_query, resultsbox, spinner, navigation_view):
        # This is weird, but basically, nuke the .tmp directory,
        # Then, if we get any error, just create it instead.
        # Technically, we don't need to create the .tmp directory here,
        # because the YouTube downloader does it automatically, but this block
        # basically does all the error handling.
        try:
            rmtree(".tmp")
            os.mkdir(".tmp")
        except:
            os.mkdir(".tmp")
        
        # Declare a `for` loop for the numbers 1-10.
        # We are going to use this to get the first 10 YouTube search results.
        # We don't download the actual audio now. That comes later.
        # Instead, we just want metadata about the video,
        # in order to show  the user what result we came back with for their query.
        for i in range(1,11):
            os.mkdir(os.path.join(".tmp", str(i)))
            
            # This is a dictionary containing runtime options for the downloader.
            ydl_search_opts = {

                # The `default-search` option lets you specify how you want to search.
                # Here, we tell it to ytsearch<i>
                # This means, grab the first "i" (ie "first 5") search results.
                # Using this functionaity, we could technically avoid using a for-loop.
                # However, we want to display the search results as they come in,
                # and if we used the "grab the first i results" by itself, the user would have to
                # wait for all of the results to come back before we could continue program flow,
                # thereby making them look at a blank screen.
                # Therefore, we use this option in combination with the next option...
                'default_search' : 'ytsearch'+str(i),

                # The `playlist_items` option here lets us get the "i"th result specifically.
                # Together with the last option, this means that for each iteration of the loop,
                # we ask for the top <i> search results, but only actually grab the "i"th.
                'playlist_items' : str(i),

                # Save the downloads to a directory called .tmp\<i>\
                # This means each search result gets a unique folder.
                'paths': {
                    'home' : os.path.join(".",".tmp", str(i))  
                },

                # Don't actually download the video itself at all.
                # Remember, right now, we just want metadata.
                'skip_download' : 'true',

                # Write the thumbnail to file
                'writethumbnail' : 'true',

                # Write the YouTube URL to file
                'writewebloclink' : 'true',

                # If it's the thumbnail, we name the output file something like
                # "IMG-videotitle.fileextension"
                # If not, don't use the `IMG` part
                'outtmpl' : {
                    'default' : '%(title)s',
                    'thumbnail' : 'IMG-%(title)s'
                }
            }
            
            # Instantiate a `YoutubeDL` object, using `ydl_search_opts` as the parameter.
            # Then, call the `download` method, passing `url` as a parameter.
            YoutubeDL(ydl_search_opts).download(search_query)

            # For the following UI elements, keep in mind that these are created for each result.
            # Their variable names are not unique outside of this for-loop.

            # First, we create a button, inside of which which the search result will be displayed.
            # It's inside a button so that the user can click on the result to go to the next step.
            # The `flat` style class makes it look cleaner.
            search_result_button = Gtk.Button()
            search_result_button.add_css_class("flat")

            # Create a box to handle the layout inside of the search result button.
            search_result_button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)

            # Declare a variable which will hold the path to the downloaded thumbnail.
            thumbnail_path = ""

            # Look in .tmp\<i>, list all the files, and iterate through them.
            for filename in os.listdir(os.path.join(".tmp",str(i))):
                # If the filename contains "IMG-", we know that it is the thumbnail.
                # This method might fail if the video title has "IMG-" in it,
                if "IMG-" in filename:
                    # Now we can save the relative path to the thumbnail
                    thumbnail_path = os.path.join(".tmp", str(i), filename)

            # Google invented a wacky file format called .webp,
            # which is the format that they use to store YouTube thumbnails.
            # Gtk doesn't play well with .webp sometimes, so let's make the images .png!
            # We're going to convert the image to .png using PIL (the Pillow package)
            # Here, we open the image we just found, as an image object,
            # Then split the filename and extension in two, in order to remove the .webp extension.
            # Then we save it as .png
            Image.open(thumbnail_path).save(os.path.splitext(thumbnail_path)[0] + ".png")

            # Delete the original unconverted thumbnail
            os.remove(thumbnail_path)

            # Update the thumbnail path to point to the new .png version
            thumbnail_path = os.path.splitext(thumbnail_path)[0] + ".png"

            # Create an image to hold the video thumbnail.
            # Then, request a size of 240p, and set the image from the path.
            # Then add the image to the result_button_box. 
            search_result_thumbnail = Gtk.Image()
            search_result_thumbnail. set_size_request(352,240)
            search_result_thumbnail.set_from_file(thumbnail_path)
            search_result_button_box.append(search_result_thumbnail)

            # The path of the file containing the URL.
            url_file_path = ""

            for filename in os.listdir(os.path.join(".tmp",str(i))):
                # If the filename contains "IMG-", we know that it is the thumbnail.
                # This method might fail if the video title has "IMG-" in it,
                if os.path.splitext(filename)[1] == ".webloc":
                    # Now we can save the relative path to the thumbnail
                    url_file_path = os.path.join(".tmp", str(i), filename)

            # Create a label to hold the title of the search result.
            # Allow the text to wrap if there is not enough space.
            # Allow it to expand if it gets more space.
            # Then, set the label based off of the filename of the url_file_path,
            # Which should just be the video title.
            # Then add it to the search results box.
            search_result_text = Gtk.Label()
            search_result_text.set_wrap(True)
            search_result_text.set_hexpand(True)
            search_result_text.set_label(os.path.splitext(os.path.split(url_file_path)[1])[0])
            search_result_button_box.append(search_result_text)

            # Set the completed search_result_button_box as the child of the search_result_button
            search_result_button.set_child(search_result_button_box)

            # Connect the search_result_button's "clicked" signal to the  `_result_clicked` callback function.
            # We pass the
            search_result_button.connect("clicked", self._result_clicked, url_file_path, thumbnail_path, navigation_view)

            # Add this result to the results
            resultsbox.append(search_result_button)
        
        # This is outside of the for-loop.
        # Getting here means we have received all 10 search results.
        # The program is done working, hide the search spinner.
        spinner.stop()

        # Return, because, if we don't, the thread never stops.
        return

    # Callback function for whenever a result is selected.
    def _result_clicked(self, button, url_file_path, thumbnail_path, navigation_view):
        navigation_view.push(pyvizcustomizerpage.PyVizCustomizerPage(url_file_path, thumbnail_path, navigation_view))
