import random

from matrix import LedMatrix


class PongGame:
    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.paddle1 = [5, 6, 7]  # Vertical positions of the paddle
        self.paddle2 = [5, 6, 7]
        self.ball = [5, 5]  # Position of the ball
        self.ball_dir = [0, 1]  # Direction of the ball
        self.score = 0

    def game_loop(self):
        while True:
            # TODO replace this line with your method for getting player input
            key = input("Enter direction (w/s): ")

            game_status = self.update(key)

            if game_status is False:  # Game over
                print("Game Over. Your Score is: ", self.score)
                break

    def update(self, key):
        # Move player paddle
        if key == "w" and 0 not in self.paddle1:
            self.paddle1 = [p - 1 for p in self.paddle1]
        elif key == "s" and self.matrix.rows - 1 not in self.paddle1:
            self.paddle1 = [p + 1 for p in self.paddle1]

        # Move opponent paddle randomly
        move = random.choice([-1, 1])
        if move == -1 and 0 not in self.paddle2:
            self.paddle2 = [p - 1 for p in self.paddle2]
        elif move == -1 and self.matrix.rows - 1 not in self.paddle2:
            self.paddle2 = [p + 1 for p in self.paddle2]

        # Move ball
        new_ball = [self.ball[0] + self.ball_dir[0], self.ball[1] + self.ball_dir[1]]

        # check if game ended
        if (new_ball[1] == 0 and new_ball[0] not in self.paddle1) or (
            new_ball[1] == self.matrix.cols - 1 and new_ball[0] not in self.paddle2
        ):
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
        if new_ball[0] == 0 or new_ball[0] == self.matrix.rows:
            self.ball_dir[0] = -self.ball_dir[0]

        # Update and draw ball position
        self.set_pixel(self.ball[0], self.ball[1], (0, 0, 0))  # black
        self.ball = [self.ball[0] + self.ball_dir[0], self.ball[1] + self.ball_dir[1]]
        self.set_pixel(self.ball[0], self.ball[1], (255, 0, 0))  # red

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

        return True
