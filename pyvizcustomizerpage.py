import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

import os

class PyVizCustomizerPage(Adw.NavigationPage):
    def __init__(self, url_file_path, thumbnail_path, navigation_view):
        super().__init__()

        self.set_title("Customize the Visualizer")

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
        
        selected_video_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        selected_video_box.set_hexpand(True)

        thumbnail_image = Gtk.Image()
        thumbnail_image.set_size_request(352,240)
        thumbnail_image.set_from_file(thumbnail_path)
        selected_video_box.append(thumbnail_image)

        selected_video_text_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 4)
        selected_video_text_box.set_valign(Gtk.Align.CENTER)

        you_have_selected_text = Gtk.Label()
        you_have_selected_text.set_halign(Gtk.Align.START)
        you_have_selected_text.set_label("You have selected...")
        selected_video_text_box.append(you_have_selected_text)

        video_title_text = Gtk.Label()
        video_title_text.set_label(os.path.splitext(os.path.split(url_file_path)[1])[0])
        video_title_text.set_halign(Gtk.Align.START)
        video_title_text.set_justify(Gtk.Justification.LEFT)
        video_title_text.set_hexpand(True)
        video_title_text.set_wrap(True)
        video_title_text.add_css_class("title-1")
        selected_video_text_box.append(video_title_text)
    
        selected_video_box.append(selected_video_text_box)

        mainbox.append(selected_video_box)

        settingsbox_clamp = Adw.Clamp()
        settingsbox_clamp.set_maximum_size(512)

        settingsbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 16)

        visualizer_selector_label = Gtk.Label()
        visualizer_selector_label.set_halign(Gtk.Align.CENTER)
        visualizer_selector_label.set_label("Choose your visualizer:")
        settingsbox.append(visualizer_selector_label)

        visualizer_selector = Adw.ViewSwitcher()
        visualizer_selector.set_margin_start(64)
        visualizer_selector.set_margin_end(64)
        visualizer_selector.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        settingsbox.append(visualizer_selector)

        visualizer_options_stack = Adw.ViewStack()

        pyviz_settings_page = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
        testlabel1 = Gtk.Label()
        testlabel1.set_label("test1")
        pyviz_settings_page.append(testlabel1)
        visualizer_options_stack.add_titled_with_icon(pyviz_settings_page, "pyviz-settings-page", "PyViz", "folder-python-symbolic")

        goom_settings_page = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)
        testlabel2 = Gtk.Label()
        testlabel2.set_label("test2")
        goom_settings_page.append(testlabel2)
        visualizer_options_stack.add_titled_with_icon (goom_settings_page, "goom-settings-page", "GOOM", "folder-music-symbolic")

        settingsbox.append(visualizer_options_stack)

        visualizer_selector.set_stack(visualizer_options_stack)

        settingsbox_clamp.set_child(settingsbox)

        mainbox.append(settingsbox_clamp)

        scrolled_window.set_child(mainbox)

        toolbar_view.set_content(scrolled_window)

        self.set_child(toolbar_view)