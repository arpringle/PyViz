# PyViz, a Python music visualizer.
# Program by Austin Pringle, Caleb Rachocki, & Caleb Ruby
# Pennsylvania Western University, California
#
# visualizerengine.py
# This file contains the our custom visualizer.
# The ♥ of the program!

# `librosa` is a musical analysis library.
# We use it for everything on the frequency analysis side of this visualizer
import librosa

# We use `numpy` for a handful of math-related calculations for the visualizer.
import numpy as np

# `pygame` is where the magic happens. It is responsible for drawing our visualizer.
import pygame

# For path.join what else
import os

class AudioAnalyzer:
    def __init__(self, filename):
        time_series, sample_rate = librosa.load(filename)
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
        self.time_index_ratio = len(times) / times[len(times) - 1]
        self.frequencies_index_ratio = len(frequencies) / frequencies[len(frequencies)-1]

    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]

class AudioBar:
    def __init__(self, x, y, freq, color, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.min_height, self.max_height = min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel)

    def update(self, dt, decibel, screen_height):
        # Calculate the desired height based on the decibel and ratio
        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        # Clamp the height to ensure it stays within the defined range
        #self.height = max(self.min_height, min(self.max_height, desired_height))

        # Update the y position to the bottom of the screen
        self.y = screen_height - self.max_height

        # Calculate the speed of height change
        speed = (desired_height - self.height) / 0.1

        # Update the height
        self.height += speed * dt

         # Clamp the height to ensure it stays within the defined range
        self.height = self.clamp(self.min_height, self.max_height, self.height)

    def render(self, screen, barWidth):
        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, barWidth, self.height))

    def clamp(self, min_value, max_value, value):
        if value < min_value:
            return min_value

        if value > max_value:
            return max_value

        return value

def run_audio_visualizer(filename, bar_color, bg_color):

    # For some godforsaken reason, the color chooser widget returns a proprietary RGB object
    # It will let you output to a string, but not a tuple... why?
    # Anyways, this is my converter between their object and a tuple. It's ugly.
    cur_colorcode = ""
    color_code_list = []
    allow = False
    counter = 0
    converted_bg_color = 0
    converted_bar_color = 0
    for rgba in (bar_color, bg_color):
        for char in rgba.to_string():
            
            if char == "(":
                allow = True
                continue

            if allow == True:

                if char == ",":
                    color_code_list.append(int(cur_colorcode))
                    cur_colorcode = ""
                    continue
                        
                if char == ")":
                    try:
                        color_code_list.append(int(cur_colorcode))

                    except ValueError:
                        pass

                    counter = counter+1

                    if counter == 1:
                        converted_bar_color = tuple(color_code_list)

                    if counter == 2:
                        converted_bg_color = tuple(color_code_list)

                    cur_colorcode = ""
                    color_code_list = []
                    allow = False
                    break


                else: cur_colorcode = cur_colorcode + char


    # Initialize audio analyzer
    anal = AudioAnalyzer(filename)

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    window_width = 800
    window_height = 600
    screen_height = window_height
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

    # Initialize array of bars
    bars = []
    frequencies = np.arange(100, 8000, 100)
    barNum = len(frequencies)

    for i, freq in enumerate(frequencies):
        x = (i * window_width) // barNum
        bars.append(AudioBar(x, 300, freq, converted_bar_color, max_height=400))

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)

    t = pygame.time.get_ticks()
    getTicksLastFrame = t
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)
    running = True
    while running:
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                for i, freq in enumerate(frequencies):
                    x = (i * event.w) // barNum
                    bars[i].x = x
                screen_height = screen.get_height()

        screen.fill(converted_bg_color)

        for i, bar in enumerate(bars):
            barWidth = window_width // barNum
            bar.update(deltaTime, anal.get_decibel(pygame.mixer.music.get_pos() / 1000.0, bar.freq), screen_height)
            bar.render(screen, barWidth)

        pygame.display.flip()

    pygame.quit()
