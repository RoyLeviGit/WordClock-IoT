import asyncio
import os
import shutil
import socket
import numpy as np
from typing import Union
from fastapi import FastAPI, File, HTTPException, UploadFile
import httpx
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
import pycountry

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
once = False
# Place your ESP32 IP
esp_ip = "172.20.10.4"

#socket
def send_commands(encoded_commands):
    try:
        # Send the commands over the network socket
        sock.sendall(encoded_commands)
    except socket.error:
        print("Refreshing socket connection:", str(socket.error))
        sock.close()
        sock.connect((esp_ip, 80))
        sock.sendall(encoded_commands)

    print(f"Sent commands:\n{encoded_commands} sock", sock)

@app.on_event("startup")
async def startup_event():
    sock.connect((esp_ip, 80))

@app.on_event("shutdown")
async def shutdown_event():
    sock.close()


# Global variables.
matrix = LedMatrix(send_commands, rows=11, cols=12, debug_no_socket=False)
# send_commands(f"C{np.random()},255,255,255\nS\n".encode())
# send_commands(f"C1,255,255,255\nS\n".encode())
current_task = None
current_clock = None
last_clock = None
current_timezone = None
current_game = None
last_game = None
gif_player = GifPlayer(matrix)
# gif_player = None

def cancel_current_task():
    global current_task, gif_player, current_game
    if current_task:
        current_task.cancel()
        current_task = None
    if gif_player:
        gif_player.stop_gif()
        # gif_player = None
    if current_game:
        current_game.stop_game()
        current_game = None

def get_current_time():
    global current_timezone
    if not current_timezone:
        return datetime.now()
    return datetime.now(current_timezone)
    
@app.get("/word-clock")
async def word_clock():
    global current_task, last_clock
    cancel_current_task()

    last_clock = "word"

    async def draw_clock_periodically():
        global current_clock
        current_clock = WordClock(matrix)

        while True:
            time_to_draw = get_current_time()
            current_clock.draw_time(time_to_draw)
            await asyncio.sleep(60)  # Wait for 1 minute

    current_task = asyncio.ensure_future(draw_clock_periodically())
    return {"message": "Word clock started."}


@app.get("/digital-clock")
async def digital_clock():
    global current_task, last_clock
    cancel_current_task()

    last_clock = "digital"

    async def draw_clock_periodically():
        global current_clock
        current_clock = DigitalClock(matrix)

        while True:
            time_to_draw = get_current_time()
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
            current_clock.color = [color_data.to_rgb()]
            current_clock.draw_time(get_current_time())

            return {"message": "Color changed successfully."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="No clock is currently running.")
    
class CountryRequest(BaseModel):
    country: str

@app.post("/change-country")
async def change_country(country_request: CountryRequest):
    global current_timezone
    
    selected_country = country_request.country
    print(f"Selected country: {selected_country}")

    try:
        country_code = pycountry.countries.search_fuzzy(selected_country)[0].alpha_2
        timezone = pytz.country_timezones[country_code][0]
        current_timezone = pytz.timezone(timezone)
    except KeyError:
        raise ValueError("Invalid country name.")

    global current_clock
    if current_clock:
        try:
            current_clock.draw_time(get_current_time())
            return {"message": "Country changed successfully."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="No clock is currently running.")

class ThemeRequest(BaseModel):
    theme: str

    def to_rgb(self):
        color_dict = {
            # Christianity
            "christmas": ["#FF0000", "#00FF00", "#FFD700"],     # Red, Green, Gold
            "easter": ["#EE82EE", "#FFFFFF", "#FFFF00"],        # Purple, White, Yellow
            "carnival": ["#FF1493", "#FFD700", "#00FFFF"],      # Deep Pink, Gold, Cyan

            # Judaism
            "hanukkah": ["#0000FF", "#C0C0C0", "#FFD700"],      # Blue, Silver, Gold
            "purim": ["#FF00FF", "#FFFF00", "#00FF00"],         # Magenta, Yellow, Green
            "sukkot": ["#FFA500", "#FFFFFF", "#8B4513"],        # Orange, White, Saddle Brown

            # Islam
            "eid-al-fitr": ["#008000", "#FFFF00", "#FFFFFF"],   # Green, Yellow, White
            "eid-al-adha": ["#8B4513", "#FFFFFF", "#FFD700"],    # Saddle Brown, White, Gold
            "milad-un-nabi": ["#008000", "#FFFFFF", "#FFD700"]   # Green, White, Gold
        }
        hex_colors = color_dict[self.theme]
        rgb_colors = []
        for color in hex_colors:
            color = color.lower()
            rgb_colors.append((
                int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16),
            ))
        return rgb_colors


@app.post("/set-theme")
async def set_theme(theme_request: ThemeRequest):
    global current_clock
    if current_clock:
        try:
            # change_color method is assumed to be async
            current_clock.color = theme_request.to_rgb()
            current_clock.draw_time(get_current_time())

            return {"message": "Theme changed successfully."}
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
async def snake_game():
    global current_task, last_game
    cancel_current_task()

    last_game = "snake"

    async def game_task():
        global current_game
        current_game = SnakeGame(matrix)
        current_game.game_loop()

    current_task = asyncio.ensure_future(game_task())

    return {"message": "Snake game started."}

@app.get("/pong-game")
async def pong_game():
    global current_task, last_game
    cancel_current_task()

    last_game = "pong"

    async def game_task():
        global current_game
        current_game = PongGame(matrix)
        current_game.game_loop()

    current_task = asyncio.ensure_future(game_task())

    return {"message": "Pong game started."}

@app.get("/game/{key}")
async def game_keypress(key: str):
    if not current_game:
        return {"message": "No game is currently running."}

    if key == "restart":
        global last_game
        if not last_game:
            return {"message": "No game is currently running."}
        
        if last_game == "snake":
            await snake_game()
        elif last_game ==  "pong":
            await pong_game()
        return {"message": "Game restarted."}
    
    if key == "exit":
        cancel_current_task()
        return {"message": "Game stopped."}

    await current_game.handle_key(key)
    return {"message": f"Processed keypress: {key} for {current_game}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
