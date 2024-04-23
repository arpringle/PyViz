# `os` is used to access files in a system-independent way.
import os

# Explanation of these imports is in the `pyvizapp.py` file
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

# This is the next page in the navigation progression.
import pyvizgoompage

# Inherit from AdNavigationPage.
class PyVizCustomizerPage(Adw.NavigationPage):

    # Constructor function. We get the thumbnail path and the nav view
    def __init__(self, thumbnail_path, navigation_view):

        # Use the parent constructor function
        super().__init__()

        # Set the title to appear at the top of the screen.
        self.set_title("Customize the Visualizer")

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
        
        # This box will be at the top of the screen.
        # It contains the video title and thumbnail.
        selected_video_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        selected_video_box.set_hexpand(True)

        # Create an image to prominently display the video thumbnail
        # Set it based on the thumbnail path
        # Add it to the `selected_video_box`
        thumbnail_image = Gtk.Image()
        thumbnail_image.set_size_request(352,240)
        thumbnail_image.set_from_file(thumbnail_path)
        selected_video_box.append(thumbnail_image)

        # Now, we have a sub-box that will hold two text labels...
        selected_video_text_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        selected_video_text_box.set_margin_end(16)
        selected_video_text_box.set_valign(Gtk.Align.CENTER)

        # ...the first of the two labels is one that says "you have selected"...
        you_have_selected_text = Gtk.Label()
        you_have_selected_text.set_halign(Gtk.Align.START)
        you_have_selected_text.set_label("You have selected...")
        selected_video_text_box.append(you_have_selected_text)

        # ...the second of the two labels is one that holds the video title.
        # We use a special style class for this one.
        video_title_text = Gtk.Label()

        # In this super fun block of code we isolate the video title from the rest of
        # the thumbnail path.
        # First, we split the filename from the path
        video_title_inprogress = os.path.split(thumbnail_path)[1]
        # Then, we excise the file extension
        video_title_inprogress = os.path.splitext(video_title_inprogress)[0]
        # Then, we tokenize the string, and remove the last token.
        # (The URL would be the last token)
        video_title_inprogress = video_title_inprogress.split()[0:len(video_title_inprogress.split())-1]
        # Then we re-unite the tokens into a string containing just the video title.
        video_title = ""
        for word in video_title_inprogress:
            video_title = video_title + word + " "
        video_title_text.set_label(video_title)
        video_title_text.set_halign(Gtk.Align.START)
        video_title_text.set_justify(Gtk.Justification.LEFT)
        video_title_text.set_hexpand(True)
        video_title_text.set_wrap(True)
        video_title_text.add_css_class("title-1")
        selected_video_text_box.append(video_title_text)
    
        # Append the box with both labels to the selected video box
        selected_video_box.append(selected_video_text_box)

        # Append the completed selected_video_box to the mainbox
        mainbox.append(selected_video_box)

        # We will soon have a box to hold visualizer settings.
        # This element strictly restricts it to a certain size
        settingsbox_clamp = Adw.Clamp()
        settingsbox_clamp.set_maximum_size(512)

        # This box holds the visualizer settings
        settingsbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 16)

        # The user can choose between our visualizer, or the open-source GOOM visualizer.
        # This label lets them know.
        visualizer_selector_label = Gtk.Label()
        visualizer_selector_label.set_halign(Gtk.Align.CENTER)
        visualizer_selector_label.set_label("Choose your visualizer:")
        settingsbox.append(visualizer_selector_label)

        # The visualizer_selector is a "view switcher", a widget that
        # Changes what is displayed on screen based off of which button is pressed.
        visualizer_selector = Adw.ViewSwitcher()
        visualizer_selector.set_margin_start(64)
        visualizer_selector.set_margin_end(64)
        visualizer_selector.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        settingsbox.append(visualizer_selector)

        # The target of a view switcher is a view stack, which contains the various
        # "views" to switch between.
        visualizer_options_stack = Adw.ViewStack()

        # The views can be any widget, but in this case,
        # we present a box with settings for the selected visualizer
        # Here is the pyviz settings page.
        pyviz_settings_page = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 32)
        testlabel1 = Gtk.Label()
        testlabel1.set_label("todo: add pyviz settings")
        pyviz_settings_page.append(testlabel1)
        visualizer_options_stack.add_titled_with_icon(pyviz_settings_page, "pyviz-settings-page", "PyViz", "audio-volume-high-symbolic")

        # Here is the goom settings page.
        goom_settings_page = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 16)

        # The first thing on the goom settings page is a description of what GOOM is.
        goom_description_label = Gtk.Label()
        goom_description_label.set_wrap(True)
        goom_description_label.set_justify(Gtk.Justification.CENTER)
        goom_description_label.set_use_markup(True)
        goom_description_label.set_label("<b><i>GOOM</i></b>  is a popular, open-source music visualizer.\nIt generates a cosmic scene based on your chosen audio.")
        goom_settings_page.append(goom_description_label)

        # Here is the nice round blue button for visualizing using GOOM.
        goom_visualize_button = Gtk.Button()
        goom_visualize_button.set_margin_start(64)
        goom_visualize_button.set_margin_end(64)
        goom_visualize_button.set_label("Visualize!")
        goom_visualize_button.add_css_class("pill")
        goom_visualize_button.add_css_class("suggested-action")

        # Retrieve the URL from the thumbnail, 
        # by taking the last token of the extensionless, pathless, file name
        url = os.path.split(thumbnail_path)[1]
        url = os.path.splitext(url)[0]
        url = url.split()
        url = url[len(url)-1]

        # When the goom visualize button is clicked, we add a new page to the navigation.
        # We pass the url and the nav view to the new page.
        goom_visualize_button.connect("clicked", self._goom_clicked, url, navigation_view)

        # Add the button to the page.
        goom_settings_page.append(goom_visualize_button)

        # Add the page to the stack
        visualizer_options_stack.add_titled_with_icon (goom_settings_page, "goom-settings-page", "GOOM", "folder-music-symbolic")

        # Add the stack to the settings box
        settingsbox.append(visualizer_options_stack)

        # Set  our newly created viewstack as the target stack of the view switcher.
        visualizer_selector.set_stack(visualizer_options_stack)

        # Set the newly finished settings box as the child of the `settingsbox_clamp`
        settingsbox_clamp.set_child(settingsbox)

        # Append the settingsbox_clamp to the mainbox
        mainbox.append(settingsbox_clamp)

        # Add the mainbox as the child of the scrolled window
        scrolled_window.set_child(mainbox)

        # Set the scrolled window as the content widget of the toolbar view.
        toolbar_view.set_content(scrolled_window)

        # Set the toolbarview as the child of this navigation view
        self.set_child(toolbar_view)

    # When the "visualize" button on the goom page is clicked, we come down here
    def _goom_clicked(self, button, url, navigation_view):
        # This nav page handles all the logic of making GOOM happen
        navigation_view.push(pyvizgoompage.PyVizGoomPage(url, navigation_view))