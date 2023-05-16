import random

from matrix import LedMatrix


class SnakeGame:
    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.snake = [(5, 5)]
        self.direction = (0, 1)  # Start moving to the right
        self.apple = self._new_apple()
        self.score = 0

    def _new_apple(self):
        while True:
            pos = (random.randint(0, 10), random.randint(0, 11))
            if pos not in self.snake:
                return pos

    def game_loop(self):
        while True:
            # TODO replace this line with your method for getting player input
            key = input("Enter direction (w/a/s/d): ")

            game_status = self.update(key)

            if game_status is False:  # Game over
                print("Game Over. Your Score is: ", self.score)
                break

    def update(self, key):
        # Update direction based on key press
        if key == "w":
            self.direction = (-1, 0)
        elif key == "a":
            self.direction = (0, -1)
        elif key == "s":
            self.direction = (1, 0)
        elif key == "d":
            self.direction = (0, 1)

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
