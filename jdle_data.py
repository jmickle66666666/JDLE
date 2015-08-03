import os
import json

TITLE = "JDLE"
SPLASH_IMAGE = "jdle_splash.png"
NO_PREVIEW = "No preview available"
UNKNOWN_LUMP = "unknown"
IDGAMES_TITLE = "idgames explorer"
IDGAMES_SCREEN_SIZE = "320x240"
IDGAMES_WAD_SCREEN_SIZE = "480x320"
JDLE_DIR = os.path.dirname(os.path.abspath(__file__))

f = open("settings.json")
settings = json.load(f)
ZDOOM_PATH = settings["zdoom_path"]
IDGAMES_MIRROR_URL = settings["idgames_mirror_url"]
SCREEN_SIZE = settings["screen_size"]
f.close()