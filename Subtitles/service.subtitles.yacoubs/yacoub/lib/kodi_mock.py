# -*- coding: utf-8 -*-
"""
Mock Kodi modules for headless testing
"""

import os
import sys

# Mock settings storage
__addon = None
__settings = {}

class Addon:
    """Mock xbmcaddon.Addon"""
    def __init__(self, id=None):
        self.id = id or 'service.subtitles.a4ksubtitles'
        self._settings = {
            # Correct setting keys based on how services access them
            'subdl.apikey': 'DxWYEw0CJsFId6lU5EM8PwfIOFijS3ND',
            'subsource.apikey': 'sk_666c7b10558b88822aead605e68a85642790c0df8dfc254a561a8b1d84a3a812',
            'opensubtitles.username': 'mohamocto@gmail.com',
            'opensubtitles.password': 'Aljedai@1010',
        }
    
    def getSetting(self, key):
        value = self._settings.get(key, '')
        return value
    
    def setSetting(self, key, value):
        self._settings[key] = str(value)
    
    def getAddonInfo(self, key):
        info = {
            'id': self.id,
            'name': 'yacoub',
            'version': '2.8.0',
            'path': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'profile': os.path.join(os.path.expanduser('~'), '.kodi', 'userdata', 'addon_data', self.id),
            'icon': '',
        }
        return info.get(key, '')
    
    def getLocalizedString(self, id):
        return f"String_{id}"

# Mock xbmc module
class XBMCModule:
    # Log levels
    LOGDEBUG = 0
    LOGINFO = 1
    LOGWARNING = 2
    LOGERROR = 3
    LOGFATAL = 4
    
    # ISO 639 language format constants
    ISO_639_1 = 0
    ISO_639_2 = 1
    ENGLISH_NAME = 2  # Add this for language name format
    
    @staticmethod
    def log(msg, level=1):
        level_names = {0: 'DEBUG', 1: 'INFO', 2: 'WARNING', 3: 'ERROR', 4: 'FATAL'}
        print(f"[XBMC-{level_names.get(level, 'INFO')}] {msg}")
    
    @staticmethod
    def translatePath(path):
        if path.startswith('special://'):
            path = path.replace('special://home/', os.path.expanduser('~/.kodi/'))
            path = path.replace('special://profile/', os.path.expanduser('~/.kodi/userdata/'))
        return path
    
    @staticmethod
    def getLanguage(format=0, region=False):
        return 'en' if format == 0 else 'English'
    
    @staticmethod
    def executeJSONRPC(json_str):
        """Mock JSON-RPC - returns empty success"""
        return '{"id":1,"jsonrpc":"2.0","result":{}}'
    
    @staticmethod
    def executebuiltin(command):
        """Mock executebuiltin - just log it"""
        print(f"[XBMC-BUILTIN] {command}")
    
    @staticmethod
    def convertLanguage(language, format):
        """Mock convertLanguage - basic conversion"""
        # Common language mappings
        lang_map = {
            'english': {'ISO_639_1': 'en', 'ISO_639_2': 'eng', 'ENGLISH_NAME': 'English'},
            'en': {'ISO_639_1': 'en', 'ISO_639_2': 'eng', 'ENGLISH_NAME': 'English'},
            'eng': {'ISO_639_1': 'en', 'ISO_639_2': 'eng', 'ENGLISH_NAME': 'English'},
            'spanish': {'ISO_639_1': 'es', 'ISO_639_2': 'spa', 'ENGLISH_NAME': 'Spanish'},
            'french': {'ISO_639_1': 'fr', 'ISO_639_2': 'fra', 'ENGLISH_NAME': 'French'},
            'german': {'ISO_639_1': 'de', 'ISO_639_2': 'deu', 'ENGLISH_NAME': 'German'},
            'italian': {'ISO_639_1': 'it', 'ISO_639_2': 'ita', 'ENGLISH_NAME': 'Italian'},
            'portuguese': {'ISO_639_1': 'pt', 'ISO_639_2': 'por', 'ENGLISH_NAME': 'Portuguese'},
            'arabic': {'ISO_639_1': 'ar', 'ISO_639_2': 'ara', 'ENGLISH_NAME': 'Arabic'},
        }
        
        lang_lower = language.lower()
        if lang_lower in lang_map:
            if format == 0:  # ISO_639_1
                return lang_map[lang_lower]['ISO_639_1']
            elif format == 1:  # ISO_639_2
                return lang_map[lang_lower]['ISO_639_2']
            elif format == 2:  # ENGLISH_NAME
                return lang_map[lang_lower]['ENGLISH_NAME']
        
        return language  # Return as-is if not found

# Mock xbmcaddon module
class XBMCAddonModule:
    Addon = Addon

# Mock xbmcvfs module
class XBMCVFSModule:
    @staticmethod
    def exists(path):
        return os.path.exists(path)
    
    @staticmethod
    def mkdir(path):
        os.makedirs(path, exist_ok=True)
        return True
    
    @staticmethod
    def mkdirs(path):
        os.makedirs(path, exist_ok=True)
        return True
    
    @staticmethod
    def translatePath(path):
        if path.startswith('special://'):
            path = path.replace('special://home/', os.path.expanduser('~/.kodi/'))
            path = path.replace('special://profile/', os.path.expanduser('~/.kodi/userdata/'))
        return path

# Mock xbmcgui module
class XBMCGUIModule:
    class ListItem:
        def __init__(self, label='', label2='', path=''):
            self.label = label
            self.label2 = label2
            self.path = path
            self.properties = {}
        
        def setProperty(self, key, value):
            self.properties[key] = value
        
        def getProperty(self, key):
            return self.properties.get(key, '')

# Mock xbmcplugin module
class XBMCPluginModule:
    SORT_METHOD_NONE = 0
    SORT_METHOD_LABEL = 1
    SORT_METHOD_UNSORTED = 40
    
    @staticmethod
    def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=0):
        """Mock addDirectoryItem"""
        return True
    
    @staticmethod
    def addSortMethod(handle, sortMethod):
        """Mock addSortMethod"""
        return True
    
    @staticmethod
    def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
        """Mock endOfDirectory"""
        return True
    
    @staticmethod
    def setResolvedUrl(handle, succeeded, listitem):
        """Mock setResolvedUrl"""
        return True

# Create module instances
xbmc = XBMCModule()
xbmcaddon = XBMCAddonModule()
xbmcvfs = XBMCVFSModule()
xbmcgui = XBMCGUIModule()
xbmcplugin = XBMCPluginModule()

# Install mocks into sys.modules
sys.modules['xbmc'] = xbmc
sys.modules['xbmcaddon'] = xbmcaddon
sys.modules['xbmcvfs'] = xbmcvfs
sys.modules['xbmcgui'] = xbmcgui
sys.modules['xbmcplugin'] = xbmcplugin

# Initialize global addon instance
__addon = Addon()

# Export everything
__all__ = ['xbmc', 'xbmcaddon', 'xbmcvfs', 'xbmcgui', 'xbmcplugin', 'Addon', '__addon']
