from PIL import Image, ImageSequence
import sys


def gif_to_frames(gif_path, output_file):
    gif = Image.open(gif_path)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        frame = frame.rotate(-90).resize(
            (11, 12), Image.LANCZOS
        )  # Resize to 12x11 pixels
        frame_rgb = list(frame.convert("RGB").getdata())
        frames.append(frame_rgb)

    with open(output_file, "w") as f:
        f.write("uint8_t gif_frames[][NUM_LEDS * 3] = {\n")
        for frame in frames:
            f.write("  { ")
            for pixel in frame:
                r, g, b = pixel
                f.write(f"{r}, {g}, {b}, ")
            f.write("},\n")
        f.write("};\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gif_to_frames.py <gif_path> <output_file>")
    else:
        gif_to_frames(sys.argv[1], sys.argv[2])
