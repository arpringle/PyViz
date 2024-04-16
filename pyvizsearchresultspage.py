import os

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

import threading

from yt_dlp import YoutubeDL

from shutil import rmtree

import pyvizcustomizerpage

class PyVizSearchResultsPage(Adw.NavigationPage):
    def __init__(self, feedback_text, submit_button, spinner, search_query, navigation_view):
        super().__init__()

        self.set_title("Search Results")

        feedback_text.set_label("")
        submit_button.set_sensitive(True)
        spinner.stop()

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)

        resultsbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)

        mainbox.append(resultsbox)

        search_spinner = Gtk.Spinner()
        search_spinner.set_size_request(32,32)
        mainbox.append(search_spinner)
        search_spinner.start()

        scrolled_window.set_child(mainbox)

        toolbar_view.set_content(scrolled_window)

        self.set_child(toolbar_view)

        searchThread = threading.Thread(target=self.searchYouTube, args=(search_query, resultsbox, search_spinner, navigation_view))
        searchThread.start()
    
    def searchYouTube(self, search_query, resultsbox, spinner, navigation_view):
        rmtree(".tmp")
        for i in range(1,11):
            ydl_search_opts = {
                'default_search' : 'ytsearch'+str(i),
                'paths': {'home' : os.path.join(".tmp", str(i))},
                'playlist_items' : str(i),
                'skip_download' : 'true',
                'outtmpl': '%(title)s [%(id)s].%(ext)s',
                'writethumbnail' : 'true'
            }
            
            YoutubeDL(ydl_search_opts).download(search_query)

            search_result_button = Gtk.Button()
            search_result_button.add_css_class("flat")

            search_result_button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)

            # This is perhaps the ugliest line of code I've ever written
            thumbnail_filename = os.listdir(os.path.join(".tmp",str(i)))[0]

            search_result_thumbnail = Gtk.Image()
            search_result_thumbnail. set_size_request(352,240)
            search_result_thumbnail.set_from_file(os.path.join(".tmp", str(i), thumbnail_filename))

            search_result_button_box.append(search_result_thumbnail)

            search_result_text = Gtk.Label()
            search_result_text.set_wrap(True)
            search_result_text.set_hexpand(True)
            display_title = ""
            for word in thumbnail_filename.split():
                if word!=(thumbnail_filename.split()[len(thumbnail_filename.split())-1]):
                    display_title = display_title + " " + word
            search_result_text.set_label(display_title)
            search_result_button_box.append(search_result_text)

            search_result_button.set_child(search_result_button_box)

            search_result_button.connect("clicked", self._result_clicked, thumbnail_filename, navigation_view)

            resultsbox.append(search_result_button)
        
        spinner.stop()

        return

    def _result_clicked(self, button, url, navigation_view):
        navigation_view.push(pyvizcustomizerpage.PyVizCustomizerPage(url))
