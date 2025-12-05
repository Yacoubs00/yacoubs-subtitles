# -*- coding: utf-8 -*-

import os
import sys

# Delete API mode env var BEFORE any imports
api_mode_env = 'A4KSUBTITLES_API_MODE'
if api_mode_env in os.environ:
    del os.environ[api_mode_env]

from yacoub import service
import importlib

if __name__ == '__main__':
    # Import api after cleaning env
    api_module = importlib.import_module('yacoub.api')
    service.start(api_module.A4kSubtitlesApi())
