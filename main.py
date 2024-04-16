# PyViz, a Python music visualizer.
# Program by Austin Pringle, Caleb Rachocki, & Caleb Ruby
# Pennsylvania Western University, California
#
# main.py
# This file instantiates the application object.

# `sys` is used to pass command-line args to the app.
# We don't use command-line arguments, but the GUI toolkit does.
import sys

# Importing the app.
import pyvizapp

# Instantiate the `PyVizApplication` object
app = pyvizapp.PyVizApplication()

# Call the `run` method on the newly-created app.
# We also pass command line arguments to the `run` method via `sys.argv`
# We don't use  these command line arguments.
# However, gtk requires access to them.
# Then, we save the exit status of the app to the variable `exit_status`
exit_status = app.run(sys.argv)

# After the app is done running, we exit the interpreter and raise the exit status via a method. 
sys.exit(exit_status)