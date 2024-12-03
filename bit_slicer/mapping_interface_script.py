# mapping interface script for bit slicer

from pathlib import Path
import sys


class Script(object):
    def __init__(self):

        # add git repo path
        try:
            git_repo_path = Path("")
            if not git_repo_path.exists():
                raise FileNotFoundError(f"Git repository path does not exist: {git_repo_path}. Please use the setup script.")
            sys.path.append(str(git_repo_path))
            debug.log(f"Added {git_repo_path} to sys.path")
        except FileNotFoundError:
            raise

        # import map module using subdirectory paths from config file
        try:
            from config import bit_slicer_path
            sys.path.append(str(bit_slicer_path))
            debug.log(f"Added {bit_slicer_path} to sys.path")

            from map_logic import MapLogic
            self.map_logic = MapLogic(vm, debug)

        except ImportError as e:
            debug.log(f"Error importing modules: {e}")
            raise

    def execute(self, delta_time):
        self.map_logic.execute(delta_time)

    def finish(self):
        self.map_logic.finish()

