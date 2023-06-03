import asyncio
from fastapi import FastAPI, HTTPException
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

def cancel_current_task():
    global current_task
    if current_task:
        current_task.cancel()
        current_task = None


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

@app.get("/play-gif")
def play_gif():
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
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
