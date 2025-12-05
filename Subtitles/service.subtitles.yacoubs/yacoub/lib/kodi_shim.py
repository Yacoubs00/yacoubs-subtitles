# kodi_shim.py — minimal shim to satisfy addon expectations when running headless
# It tries to reuse the bundled kodi_mock, but provides fallback implementations
# for Addon and other commonly used Kodi APIs so imports never fail.

import types
try:
    from . import kodi_mock as _kodi_mock
except Exception:
    _kodi_mock = None

class AddonShim:
    def __init__(self, id=None):
        # if kodi_mock exposes a backing __addon object, reuse it
        if _kodi_mock and hasattr(_kodi_mock, "__addon"):
            self._impl = getattr(_kodi_mock, "__addon")
        else:
            self._impl = None
        self.id = id or "service.subtitles.a4ksubtitles"
    def getSetting(self, key):
        try:
            if self._impl and hasattr(self._impl, "getSetting"):
                return self._impl.getSetting(key)
        except Exception:
            pass
        return ""
    def getSettingBool(self, key):
        v = self.getSetting(key)
        return str(v).lower() in ("1","true","yes","on")
    def setSetting(self, key, value):
        try:
            if self._impl and hasattr(self._impl, "setSetting"):
                return self._impl.setSetting(key, value)
        except Exception:
            pass
        return None
    def getAddonInfo(self, key):
        try:
            if self._impl and hasattr(self._impl, "getAddonInfo"):
                return self._impl.getAddonInfo(key)
        except Exception:
            pass
        if key == "id":
            return self.id
        return ""

# Provide simple stubs for other xbmc* APIs expected by the code
class _StubModule(types.SimpleNamespace):
    def __init__(self):
        super().__init__()
    def log(self, *args, **kwargs):
        # noop or print to stdout for debug
        try:
            print("[kodi_shim.log]", *args, **kwargs)
        except Exception:
            pass

# Build a module-like object to expose to sys.modules
_kshim = _StubModule()
_kshim.Addon = AddonShim
# expose common helper names (kodi_mock sometimes uses xbmc.LOGDEBUG etc)
for attr in ("LOGDEBUG", "LOGINFO", "LOGERROR", "LOGWARNING"):
    if not hasattr(_kshim, attr):
        setattr(_kshim, attr, 0)

# expose convenient attributes used by scripts
_kshim.kodi_mock = _kodi_mock
# If kodi_mock provided xbmc-like attributes, copy some over if present
if _kodi_mock:
    for a in dir(_kodi_mock):
        if not hasattr(_kshim, a):
            try:
                setattr(_kshim, a, getattr(_kodi_mock, a))
            except Exception:
                pass

# Provide module-level helpers used by code: xbmc.translatePath or xbmcvfs.* can be delegated
def translatePath(path):
    # simple passthrough
    return path

_kshim.translatePath = translatePath

# Make the shim importable as a module object via standard import
# The file's top-level defines the actual attributes used by the wrapper when mapping sys.modules
# End of kodi_shim.py
