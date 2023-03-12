import pathlib
import subprocess


class Editor:

    DEFAULT_CMD = "vim"

    def __init__(self, cmd: str | None) -> None:
        self._cmd = cmd or Editor.DEFAULT_CMD

    def open(self, path: pathlib.Path) -> None:
        subprocess.call([self._cmd, path.as_posix()])
