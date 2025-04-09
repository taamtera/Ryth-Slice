class Rythm:
    def __init__(self, bpm):
        self.current_beat = 0
        self.bpm = bpm

    def tick(self, ticks):
        self.current_beat = ticks / (60000 / self.bpm)
        return self.current_beat
