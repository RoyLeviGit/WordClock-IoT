from datetime import datetime

from matrix import LedMatrix


class DigitalClock:
    NUMBERS = {
        "0": ["###", "# #", "# #", "# #", "###"],
        "1": ["  #", "  #", "  #", "  #", "  #"],
        "2": ["###", "  #", "###", "#  ", "###"],
        "3": ["###", "  #", "###", "  #", "###"],
        "4": ["# #", "# #", "###", "  #", "  #"],
        "5": ["###", "#  ", "###", "  #", "###"],
        "6": ["###", "#  ", "###", "# #", "###"],
        "7": ["###", "  #", "  #", "  #", "  #"],
        "8": ["###", "# #", "###", "# #", "###"],
        "9": ["###", "# #", "###", "  #", "###"],
    }

    def __init__(self, matrix: LedMatrix):
        self.matrix = matrix
        self.matrix.clear()
        self.color = (255, 255, 255)

    def draw_char(self, char, x, y, color):
        for i, line in enumerate(self.NUMBERS[char]):
            for j, pixel in enumerate(line):
                if pixel == "#":
                    self.matrix.set_pixel(x + i, y + j, color)

    def draw_time(self, time_to_draw: datetime):
        hour_str = time_to_draw.strftime("%H")
        min_str = time_to_draw.strftime("%M")

        x_h, y_h = 0, 2  # Start position for hours (top middle)
        x_m, y_m = 6, 2  # Start position for minutes (bottom middle)

        # Draw hours
        for char in hour_str:
            self.draw_char(char, x_h, y_h, self.color)
            y_h += 5  # Move to the right. We add 4 because the width of each character is 3, and we leave 1 column for spacing

        # Draw minutes
        for char in min_str:
            self.draw_char(char, x_m, y_m, self.color)
            y_m += 5  # Move to the right. We add 4 because the width of each character is 3, and we leave 1 column for spacing

        self.matrix.show()
