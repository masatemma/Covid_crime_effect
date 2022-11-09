import os

def make_dir():
    ROOT_DIR = os.path.dirname(os.path.abspath("main.py"))

    vis_folder = 'visualisations'
    wrangle_folder = 'wrangled'

    vis_path = os.path.join(ROOT_DIR, vis_folder)
    data_path = os.path.join(ROOT_DIR, wrangle_folder)

    paths = [vis_path, data_path]

    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
