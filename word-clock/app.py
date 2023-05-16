from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from game import SnakeGame, PongGame
from gif import GifPlayer
from gif import GifStore
from clock import DigitalClock, WordClock
from matrix import LedMatrix

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set the allowed origins here. Use ["*"] to allow all origins.
    allow_credentials=True,
    allow_methods=["*"],  # Set the allowed HTTP methods here.
    allow_headers=["*"],  # Set the allowed headers here.
)

@app.get("/word-clock")
def word_clock():
    matrix = LedMatrix(ip_address="172.20.10.2", rows=11, cols=12)

    time_to_draw = datetime.now()
    clock = WordClock(matrix)
    clock.draw_time(time_to_draw)
    sleep(1)
    return {"message": "Word clock drawn."}

@app.get("/digital-clock")
def digital_clock():
    matrix = LedMatrix(ip_address="172.20.10.2", rows=11, cols=12)

    time_to_draw = datetime.now()
    clock = DigitalClock(matrix)
    clock.draw_time(time_to_draw)
    sleep(2)
    return {"message": "Digital clock drawn."}

@app.get("/play-gif")
def play_gif():
    matrix = LedMatrix(ip_address="172.20.10.2", rows=11, cols=12)

    player = GifPlayer(matrix)
    gif_store = GifStore("word-clock/gif/gifs")
    for gif in gif_store.gif_paths:
        player.play_gif(gif)
        sleep(3)
        player.stop_gif()  # To stop playing gif
    sleep(1)
    return {"message": "Gifs played."}

@app.get("/snake-game")
def snake_game():
    s_game = SnakeGame(matrix)
    s_game.game_loop()
    sleep(1)
    return {"message": "Snake game started."}

@app.get("/pong-game")
def pong_game():
    s_game = PongGame(matrix)
    s_game.game_loop()
    return {"message": "Pong game started."}

@app.get("/game/{game_name}/keypress/{key}")
def game_keypress(game_name: str, key: str):
    if game_name == "snake":
        game = SnakeGame(matrix)
    elif game_name == "pong":
        game = PongGame(matrix)
    else:
        return {"message": f"No game found with name: {game_name}"}

    game.process_keypress(key)
    return {"message": f"Processed keypress: {key} for {game_name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="172.20.10.3", port=8000, reload=True)
