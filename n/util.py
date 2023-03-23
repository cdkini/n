from __future__ import annotations

import os
import pathlib
import subprocess

GREP = "rg"


def grep(target: pathlib.Path, args: tuple[str, ...]) -> None:
    command = [GREP]
    for arg in args:
        command.append(arg)
    command.append(target.as_posix())
    subprocess.call(command)


def cd(path: pathlib.Path) -> None:
    os.chdir(path)
