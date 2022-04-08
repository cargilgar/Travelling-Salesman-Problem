from pathlib import Path

ROOT_DIR = Path(__file__).parents[3]


def get_abs_path(*path):
    return ROOT_DIR.joinpath(*path)
