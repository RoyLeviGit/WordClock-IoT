from PIL import Image, ImageSequence
import time
import threading

from matrix import LedMatrix


class GifPlayer:
    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.is_playing = False
        self.thread = None

    def gif_to_matrix(self, gif_path):
        gif = Image.open(gif_path)
        frames = []

        for frame in ImageSequence.Iterator(gif):
            frame = frame.rotate(90).resize(
                (self.matrix.rows, self.matrix.cols), Image.LANCZOS
            )  # Resize to self.matrix.rows*self.matrix.cols pixels
            frame_rgb = list(frame.convert("RGB").getdata())
            frames.append(frame_rgb)

        return frames

    def play_gif(self, gif_path, frame_duration=0.5):
        self.is_playing = True
        frames = self.gif_to_matrix(gif_path)

        def loop_frames():
            while self.is_playing:
                for frame in frames:
                    if not self.is_playing:
                        break
                    for i in range(self.matrix.rows):
                        for j in range(self.matrix.cols):
                            self.matrix.set_pixel(i, j, frame[j * self.matrix.rows + i])
                    self.matrix.show()
                    time.sleep(frame_duration)  # Delay between frames

        self.thread = threading.Thread(target=loop_frames)
        self.thread.start()

    def stop_gif(self):
        self.is_playing = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
