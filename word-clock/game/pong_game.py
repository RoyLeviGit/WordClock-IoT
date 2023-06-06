import asyncio
import random
import threading
from time import sleep
import time

from matrix import LedMatrix


class PongGame:
    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.matrix.clear()
        self.paddle1 = [5, 6, 7]  # Vertical positions of the paddle
        self.paddle2 = [5, 6, 7]
        self.ball = [5, 5]  # Position of the ball
        self.ball_dir = [0, 1]  # Direction of the ball
        self.score = 0
        self.is_playing = False
        self.thread = None

    async def handle_key(self, key):
        # Move player paddle
        if key == "up" and 0 not in self.paddle1:
            self.paddle1 = [p - 1 for p in self.paddle1]
        elif key == "down" and self.matrix.rows - 1 not in self.paddle1:
            self.paddle1 = [p + 1 for p in self.paddle1]

    def game_loop(self):
        self.is_playing = True

        def loop_game():
            while True:
                start_time = time.time()

                if not self.is_playing:
                    break

                game_status = self.update()

                if game_status is False:  # Game over
                    print("Game Over. Your Score is: ", self.score)
                    break

                elapsed_time = time.time() - start_time
                if elapsed_time < 0.5:
                    sleep(0.5 - elapsed_time)

        
        self.thread = threading.Thread(target=loop_game)
        self.thread.start()

    def stop_game(self):
        self.is_playing = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def update(self):
        if self.ball[1] == self.matrix.cols - 2:
            # Make last opponent paddle move random
            last_move = random.choice([-1, 0, 1])
            if last_move == 1 and self.paddle2[2] < self.matrix.rows - 1:
                self.paddle2 = [p + 1 for p in self.paddle2]
            elif last_move == -1 and self.paddle2[0] > 0:
                self.paddle2 = [p - 1 for p in self.paddle2]
        else:
            # Move opponent paddle to hit ball
            future_ball_position = self.predict_ball_position()
            if self.paddle2[1] < future_ball_position and self.paddle2[2] < self.matrix.rows - 1:
                self.paddle2 = [p + 1 for p in self.paddle2]
            elif self.paddle2[1] > future_ball_position and self.paddle2[0] > 0:
                self.paddle2 = [p - 1 for p in self.paddle2]

        # Move ball
        new_ball = [self.ball[0] + self.ball_dir[0], self.ball[1] + self.ball_dir[1]]

        # check if game ended
        if (new_ball[1] == 0 and new_ball[0] not in self.paddle1) or (
            new_ball[1] == self.matrix.cols - 1 and new_ball[0] not in self.paddle2
        ):
            self.matrix.clear()
            return False

        # Check for collisions with the paddles
        if new_ball[1] == 0 and new_ball[0] in self.paddle1:
            self.score += 1
            self.ball_dir[1] = 1
            if new_ball[0] == self.paddle1[0]:  # top of paddle
                self.ball_dir[0] = -1
            elif new_ball[0] == self.paddle1[2]:  # bottom of paddle
                self.ball_dir[0] = 1
            else:  # middle of paddle
                self.ball_dir[0] = 0
        elif new_ball[1] == self.matrix.cols - 1 and new_ball[0] in self.paddle2:
            self.score += 1
            self.ball_dir[1] = -1
            if new_ball[0] == self.paddle2[0]:  # top of paddle
                self.ball_dir[0] = -1
            elif new_ball[0] == self.paddle2[2]:  # bottom of paddle
                self.ball_dir[0] = 1
            else:  # middle of paddle
                self.ball_dir[0] = 0

        # Check for collisions with the top and bottom of the screen
        if new_ball[0] == -1 or new_ball[0] == self.matrix.rows:
            self.ball_dir[0] = -self.ball_dir[0]

        # Update and draw ball position
        self.matrix.set_pixel(self.ball[0], self.ball[1], (0, 0, 0))  # black
        self.ball = [self.ball[0] + self.ball_dir[0], self.ball[1] + self.ball_dir[1]]
        self.matrix.set_pixel(self.ball[0], self.ball[1], (255, 0, 0))  # red

        # Draw paddles
        for i in range(self.matrix.rows):
            if i in self.paddle1:
                self.matrix.set_pixel(i, 0, (255, 255, 255))  # white
            else:
                self.matrix.set_pixel(i, 0, (0, 0, 0))  # black
            if i in self.paddle2:
                self.matrix.set_pixel(i, self.matrix.cols - 1, (255, 255, 255))  # white
            else:
                self.matrix.set_pixel(i, self.matrix.cols - 1, (0, 0, 0))  # black

        self.matrix.show()

        return True
    
    def predict_ball_position(self):
        # If the ball is moving away from paddle2, return middle position as best guess
        if self.ball_dir[1] != 1:
            return self.matrix.rows // 2

        future_ball_position = self.ball[0]
        future_ball_dir = self.ball_dir[0]

        # Calculate future ball position
        for _ in range(self.matrix.cols - self.ball[1] - 1):
            future_ball_position += future_ball_dir

            # Handle bouncing off top and bottom
            if future_ball_position >= self.matrix.rows or future_ball_position < 0:
                future_ball_dir *= -1

        return future_ball_position

