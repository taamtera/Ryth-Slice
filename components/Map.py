import json
import os
import pygame  # Add this import for Pygame
from .Rythm import Rythm

# Path to the folder containing JSON files
folder_path = os.path.join(os.path.dirname(__file__), "maps")

class Map:
    def __init__(self, SlimeManager, g_grav, g_spd, spawn_ahead):
        self.SlimeManager = SlimeManager
        self.map = None
        self.beat_index = 0
        self.Rythm = None
        self.g_grav = g_grav
        self.g_spd = g_spd
        self.spawn_ahead = 10
        pygame.mixer.init()  # Initialize the Pygame mixer
        self.music_channel = None  # Add a channel for music playback
        self.last_beat = None

    def loadMaps(self):
        maps = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                maps.append(filename)
        return maps

    def selectMap(self, filename):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            obj = json.loads(file.read())
            self.map = obj
            self.Rythm = Rythm(obj["bpm"])
            self.beat_index = 0
            self.loadSound(obj["sound"])
            self.last_beat = obj["map_data"][-1]["b"]

    def loadSound(self, filename):
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)  # Load the music file
            pygame.mixer.music.play(-1)  # Play the music in a loop
        else:
            print(f"Sound file {filename} not found.")

    def stopMusic(self):
        pygame.mixer.music.stop()  # Stop the music playback

    def tick(self, ticks):
        if self.Rythm:
            current_beat = self.Rythm.tick(ticks)
            beat_group = self.getNextBeatGoup(current_beat)
            if beat_group:
                for beat in beat_group:
                    self.SlimeManager.spawn(beat["p"], beat["b"], self.map["gravity"] * self.g_grav, self.map["speed"] * self.g_spd)
            return current_beat
        return None

    def getNextBeatGoup(self, current_beat):
        beat_group = []
        while self.beat_index <= len(self.map["map_data"]) - 1 and self.map["map_data"][self.beat_index]["b"] <= current_beat + 10:
            beat_group.append(self.map["map_data"][self.beat_index])
            self.beat_index += 1
        return beat_group
