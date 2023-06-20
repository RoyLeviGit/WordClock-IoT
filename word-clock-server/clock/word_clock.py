from datetime import datetime

from matrix import LedMatrix


class WordClock:
    def __init__(self, matrix: LedMatrix):
        # Grid of the word clock
        self.grid = [
            "ITLISASTHPMA",
            "ACFIFTEENDCO",
            "TWENTYFIVEXW",
            "THIRTYFTENOS",
            "MINUTESETOUR",
            "PASTORUFOURT",
            "SEVENXTWELVE",
            "NINEFIVECTWO",
            "EIGHTFELEVEN",
            "SIXTHREEONEG",
            "TENSEZOCLOCK",
        ]
        self.matrix = matrix
        self.matrix.clear()
        self.color = [(255, 255, 255)]

    def draw_time(self, time_to_draw: datetime):
        hour = time_to_draw.hour
        minute = time_to_draw.minute
        words = self._words_to_light(hour, minute)

        # Set pixels for the words to light up
        self.matrix.clear()

        for word in words:
            pixel_indexes = self._get_pixel_index(word)
            for index in pixel_indexes:
                self.matrix.set_pixel(index[0], index[1], self.color[index[0] % len(self.color)])
        
        self.matrix.show()

    def _get_pixel_index(self, word):
        r = False
        if word == "FFIVE":
            word = "FIVE"
            r = True
        if word == "TTEN":
            word = "TEN"
            r = True

        for i in (reversed(range(len(self.grid))) if r else range(len(self.grid))):
            start = self.grid[i].find(word)
            if start != -1:
                return [(i, j) for j in range(start, start + len(word))]
        return []

    @staticmethod
    def _words_to_light(hour, minute):
        # Calculate which words to light up
        words_to_light = ["IT", "IS"]
        if minute < 5:
            words_to_light += ["OCLOCK"]
        elif minute < 10:
            words_to_light += ["FIVE", "MINUTES", "PAST"]
        elif minute < 15:
            words_to_light += ["TEN", "MINUTES", "PAST"]
        elif minute < 20:
            words_to_light += ["FIFTEEN", "PAST"]
        elif minute < 25:
            words_to_light += ["TWENTY", "MINUTES", "PAST"]
        elif minute < 30:
            words_to_light += ["TWENTY", "FIVE", "MINUTES", "PAST"]
        elif minute < 35:
            words_to_light += ["THIRTY", "MINUTES", "PAST"]
        elif minute < 40:
            words_to_light += ["TWENTY", "FIVE", "MINUTES", "TO"]
        elif minute < 45:
            words_to_light += ["TWENTY", "MINUTES", "TO"]
        elif minute < 50:
            words_to_light += ["FIFTEEN", "TO"]
        elif minute < 55:
            words_to_light += ["TEN", "MINUTES", "TO"]
        else:
            words_to_light += ["FIVE", "MINUTES", "TO"]

        # If it's half past the hour or later, we'll talk about the next hour
        if minute >= 35:
            hour += 1

        # Add the correct hour to the list of words to light up
        if hour == 1 or hour == 13:
            words_to_light.append("ONE")
        elif hour == 2 or hour == 14:
            words_to_light.append("TWO")
        elif hour == 3 or hour == 15:
            words_to_light.append("THREE")
        elif hour == 4 or hour == 16:
            words_to_light.append("FOUR")
        elif hour == 5 or hour == 17:
            words_to_light.append("FFIVE")
        elif hour == 6 or hour == 18:
            words_to_light.append("SIX")
        elif hour == 7 or hour == 19:
            words_to_light.append("SEVEN")
        elif hour == 8 or hour == 20:
            words_to_light.append("EIGHT")
        elif hour == 9 or hour == 21:
            words_to_light.append("NINE")
        elif hour == 10 or hour == 22:
            words_to_light.append("TTEN")
        elif hour == 11 or hour == 23:
            words_to_light.append("ELEVEN")
        else:  # hour == 12 or hour == 0
            words_to_light.append("TWELVE")

        return words_to_light
