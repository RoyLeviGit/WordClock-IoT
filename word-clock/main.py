from time import sleep
from datetime import datetime

from gif.gif_player import GifPlayer
from gif.gif_store import GifStore
from clock import DigitalClock, WordClock
from matrix.led_matrix import LedMatrix

matrix = LedMatrix(ip_address="10.0.0.28", rows=11, cols=12)

while True:
    option = input("Enter option (w: Word Clock, d: Digital Clock, g: Gif,  r: Clear, q: Quit): ")
    if option == "w":
        time_to_draw = datetime.now()
        clock = WordClock(matrix)
        clock.draw_time(time_to_draw)
    if option == "d":
        time_to_draw = datetime.now()
        clock = DigitalClock(matrix)
        clock.draw_time(time_to_draw)
    elif option == "g":
        player = GifPlayer(matrix)
        gif_store = GifStore("word-clock/gif/gifs")
        print(gif_store.gif_paths)
        for gif in gif_store.gif_paths:
            player.play_gif(gif)
            sleep(3)
            player.stop_gif()  # To stop playing gif
    elif option == "r":
        matrix.clear()
    elif option == "q":
        break
