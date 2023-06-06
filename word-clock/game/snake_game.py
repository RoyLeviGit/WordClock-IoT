import random
import threading
from time import sleep

from matrix import LedMatrix


class SnakeGame:
    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.matrix.clear()
        self.snake = [(5, 5)]
        self.direction = (0, 1)  # Start moving to the right
        self.apple = self._new_apple()
        self.score = 0
        self.is_playing = False
        self.thread = None

    def _new_apple(self):
        while True:
            pos = (random.randint(0, 10), random.randint(0, 11))
            if pos not in self.snake:
                return pos
            
    def handle_key(self, key):
        # Update direction based on key press
        if key == "up":
            self.direction = (-1, 0)
        elif key == "left":
            self.direction = (0, -1)
        elif key == "down":
            self.direction = (1, 0)
        elif key == "right":
            self.direction = (0, 1)
        print(f"Direction: {self.direction}")

    def game_loop(self):
        self.is_playing = True

        def loop_game():
            while True:
                if not self.is_playing:
                    break
                
                game_status = self.update()

                if game_status is False:  # Game over
                    print("Game Over. Your Score is: ", self.score)
                    break

                sleep(0.4)
        
        self.thread = threading.Thread(target=loop_game)
        self.thread.start()

    def stop_game(self):
        self.is_playing = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def update(self):
        # Move snake
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Check for collisions with the boundary
        if (
            new_head[0] < 0
            or new_head[0] >= self.matrix.rows
            or new_head[1] < 0
            or new_head[1] >= self.matrix.cols
        ):
            self.matrix.clear()
            return False

        # Check for collisions with self
        if new_head in self.snake:
            self.matrix.clear()
            return False

        self.snake.insert(0, new_head)

        # Check for apple
        if new_head == self.apple:
            self.score += 1
            self.apple = self._new_apple()
        else:
            # Remove tail if no apple was eaten
            tail = self.snake.pop()
            self.matrix.set_pixel(tail[0], tail[1], (0, 0, 0))  # black

        # Draw head
        self.matrix.set_pixel(new_head[0], new_head[1], (0, 0, 255))  # blue

        # Draw body
        for part in self.snake[1:]:
            self.matrix.set_pixel(part[0], part[1], (0, 255, 0))  # green

        # Draw apple
        self.matrix.set_pixel(self.apple[0], self.apple[1], (255, 0, 0))  # red

        self.matrix.show()

        return True
