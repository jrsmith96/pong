import cx_Freeze

executables = [cx_Freeze.Executable("pong.py")]

cx_Freeze.setup(
  name="Pong",
  options={"build_exe": {"packages": ["pygame"], "include_files": ["sounds/pong_bounce.ogg", "sounds/pong_victory.ogg"]}},
  executables=executables
)