import os
import json

f = open("settings.json")
settings = json.load(f)

TITLE = "JDLE"
SCREEN_SIZE = settings["screen_size"]
SPLASH_IMAGE = "jdle_splash.png"
NO_PREVIEW = "No preview available"
UNKNOWN_LUMP = "unknown"
IDGAMES_TITLE = "idgames explorer"
IDGAMES_SCREEN_SIZE = "320x240"
IDGAMES_WAD_SCREEN_SIZE = "480x320"
IDGAMES_MIRROR_URL = "http://ftp.ntua.gr/pub/vendors/idgames/"
JDLE_DIR = os.path.dirname(os.path.abspath(__file__))
ZDOOM_PATH = settings["zdoom_path"]