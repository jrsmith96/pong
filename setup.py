#!/usr/bin/env python3
"""Script to create executable of game"""

import cx_Freeze

executables = [cx_Freeze.Executable("pong.py")] # pylint: disable = invalid-name

cx_Freeze.setup(
  name="Pong",
  options={
    "build_exe": {
      "packages": ["pygame"],
      "include_files": [
        "sounds/pong_bounce.ogg",
        "sounds/pong_victory.ogg"
      ]
    }
  },
  executables=executables
)
