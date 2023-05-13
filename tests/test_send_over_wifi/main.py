import socket


def send_command(ip, port, commands):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(commands.encode())
        print(f"Sent commands: {commands}")


if __name__ == "__main__":
    IP_ADDRESS = "192.168.1.103"
    PORT = 80

    # Example command: set pixel 1 to green (0, 255, 0)
    commands = ""
    for i in range(132):
        single_pixel_command = f"C{i},0,255,0\n"
        commands += single_pixel_command
    commands += "S\n"

    # send_command(IP_ADDRESS, PORT, commands)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP_ADDRESS, PORT))
        for i in range(10):
            s.sendall(commands.encode())
            print(f"Sent commands: {commands}")
