from pathlib import Path

ROOT_DIR = Path(__file__).parents[3]


def get_abs_path(*path):
    """
    Get absolute path from a given file based on the root directory of the project
    """
    return ROOT_DIR.joinpath(*path)
