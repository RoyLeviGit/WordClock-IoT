import asyncio
import os
import shutil
from typing import Union
from fastapi import FastAPI, File, HTTPException, UploadFile
import httpx
from pydantic import BaseModel
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

matrix = LedMatrix(ip_address="172.20.10.2", rows=11, cols=12, debug_no_socket=True)

# Global variables.
current_task = None
current_clock = None
gif_player = GifPlayer(matrix)

def cancel_current_task():
    global current_task, gif_player
    if current_task:
        current_task.cancel()
        current_task = None
    gif_player.stop_gif()


@app.get("/word-clock")
async def word_clock():
    global current_task
    cancel_current_task()

    async def draw_clock_periodically():
        global current_clock
        while True:
            time_to_draw = datetime.now()
            current_clock = WordClock(matrix)
            current_clock.draw_time(time_to_draw)
            await asyncio.sleep(60)  # Wait for 1 minute

    current_task = asyncio.ensure_future(draw_clock_periodically())
    return {"message": "Word clock started."}


@app.get("/digital-clock")
async def digital_clock():
    global current_task
    cancel_current_task()

    async def draw_clock_periodically():
        global current_clock
        while True:
            time_to_draw = datetime.now()
            current_clock = DigitalClock(matrix)
            current_clock.draw_time(time_to_draw)
            await asyncio.sleep(60)  # Wait for 1 minute

    current_task = asyncio.ensure_future(draw_clock_periodically())
    return {"message": "Digital clock started."}

class Color(BaseModel):
    color: str

    def to_rgb(self):
        return (
            int(self.color[1:3], 16),
            int(self.color[3:5], 16),
            int(self.color[5:7], 16),
        )

@app.post("/send-color")
async def send_color(color_data: Color):
    global current_clock
    if current_clock:
        try:
            # change_color method is assumed to be async
            current_clock.color = color_data.to_rgb()
            current_clock.draw_time(datetime.now())
            return {"message": "Color changed successfully."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="No clock is currently running.")

class GifUrl(BaseModel):
    gifUrl: str

    async def download_file(self, filename):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.gifUrl)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)

@app.post("/gif_url")
async def send_gif_url(gif_data: GifUrl):
    global gif_player
    cancel_current_task()

    downloaded_gifs_directory = "downloaded_gifs"
    if not os.path.exists(downloaded_gifs_directory):
        os.makedirs(downloaded_gifs_directory)
    filename = os.path.join(downloaded_gifs_directory, os.path.basename(gif_data.gifUrl))

    await gif_data.download_file(filename)
    gif_player.play_gif(filename)

    return {"message": "Gif played."}

@app.post("/gif")
async def send_gif(gif: UploadFile = File(...)):
    global gif_player
    cancel_current_task()

    downloaded_gifs_directory = "downloaded_gifs"
    if not os.path.exists(downloaded_gifs_directory):
        os.makedirs(downloaded_gifs_directory)
    filename = os.path.join(downloaded_gifs_directory, gif.filename)

    # save the file
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(gif.file, buffer)

    gif_player.play_gif(filename)

    return {"message": "Gif played."}

@app.get("/snake-game")
def snake_game():
    global current_task
    cancel_current_task()

    async def game_task():
        global current_game
        current_game = SnakeGame(matrix)
        current_game.game_loop()

    current_task = asyncio.ensure_future(game_task())

    return {"message": "Snake game started."}

@app.get("/pong-game")
def pong_game():
    global current_task
    cancel_current_task()

    async def game_task():
        global current_game
        current_game = PongGame(matrix)
        current_game.game_loop()

    current_task = asyncio.ensure_future(game_task())

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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
