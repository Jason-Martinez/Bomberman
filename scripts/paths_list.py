import os
def get_path(path):
    extension = ('.png', '.jpg', '.jpeg', '.mp3', '.wav')
    path_imgs = [
        os.path.join(path, file)
        for file in os.listdir(path)
        if os.path.isfile(os.path.join(path, file)) and file.lower().endswith(extension)
    ]
    return path_imgs