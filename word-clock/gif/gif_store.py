import os

class GifStore:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.gif_paths = self._scan_for_gifs()

    def _scan_for_gifs(self):
        gif_paths = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                # if file.endswith('.gif'):
                gif_paths.append(os.path.join(root, file))
        return gif_paths

    def get_gif(self, index):
        if index < len(self.gif_paths):
            return self.gif_paths[index]
        else:
            print(f"No gif found at index {index}")
            return None
