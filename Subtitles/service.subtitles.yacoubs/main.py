# -*- coding: utf-8 -*-

import os
import sys

# Add lib folder to Python path for BeautifulSoup and other dependencies
addon_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(addon_path, 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Delete API mode env var BEFORE any imports
api_mode_env = 'A4KSUBTITLES_API_MODE'
if api_mode_env in os.environ:
    del os.environ[api_mode_env]

# Now import - kodi.py will check env var and use real modules
import importlib
if __name__ == '__main__':
    core_module = importlib.import_module('yacoub.core')
    core_module.main(int(sys.argv[1]), sys.argv[2][1:])
