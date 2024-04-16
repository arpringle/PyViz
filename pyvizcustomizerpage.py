import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import GLib, Gtk, Adw

class PyVizCustomizerPage(Adw.NavigationPage):
    def __init__(self, url):
        super().__init__()

        self.set_title("Customize the Visualizer")

        toolbar_view = Adw.ToolbarView()

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        mainbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 8)

        scrolled_window.set_child(mainbox)

        toolbar_view.set_content(scrolled_window)

        self.set_child(toolbar_view)