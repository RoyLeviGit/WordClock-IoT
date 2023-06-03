import socket


class LedMatrix:
    def __init__(self, ip_address, port=80, rows=11, cols=12, debug_no_socket=False):
        self.ip_address = ip_address
        self.port = port
        self.rows = rows
        self.cols = cols
        self.pixels = [(0, 0, 0)] * (rows * cols)
        self.last_pixels = [(1, 1, 1)] * (rows * cols)
        self.debug_no_socket = debug_no_socket
        self.socket = self._get_socket()
        self.show()

    def _get_socket(self):
        if self.debug_no_socket:
            return None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip_address, self.port))
        return sock

    def get_pixel(self, i, j):
        index = self._get_pixel_index(i, j)
        return self.pixels[index]

    def set_pixel(self, i, j, color):
        index = self._get_pixel_index(i, j)
        self.pixels[index] = color

    def clear(self):
        self.pixels = [(0, 0, 0)] * (self.rows * self.cols)
        self.last_pixels = [(1, 1, 1)] * (self.rows * self.cols)

    def reset(self):
        self.clear()
        self.show()

    def show(self):
        # Generate commands to set the color of each pixel
        print("Will show led matrix")
        commands = ""
        for i in range(self.rows):
            for j in range(self.cols):
                pixel_index = self._get_pixel_index(i, j)
                r, g, b = self.pixels[pixel_index]
                if self.pixels[pixel_index] != self.last_pixels[pixel_index]:
                    command = f"C{pixel_index},{r},{g},{b}\n"
                    commands += command
                    self.last_pixels[pixel_index] = self.pixels[pixel_index]
        if commands:
            commands += "S\n"
            # print(f"Sending:\n{commands}")
            if self.debug_no_socket:
                return

            try:
                # Send the commands over the network socket
                self.socket.sendall(commands.encode())
                # print(f"Sent commands:\n{commands}")
            except socket.error:
                print("Refreshing socket connection")
                self.socket.close()
                # perform reconnection
                self.socket = self._get_socket()

                self.socket.sendall(commands.encode())
                # print(f"Sent commands:\n{commands}")

    def _get_pixel_index(self, i, j):
        if i % 2 == 0:
            # Even rows go left to right
            return i * self.cols + j
        else:
            # Odd rows go right to left
            return (i + 1) * self.cols - j - 1
