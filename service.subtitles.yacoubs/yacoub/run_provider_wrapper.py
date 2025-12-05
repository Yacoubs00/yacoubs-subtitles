# --- kodi shim mapping injected by assistant ---
try:
    from yacoub.lib import kodi_shim as _kodi_shim
    for _name in ["xbmc","xbmcaddon","xbmcvfs","xbmcplugin","xbmcgui","xbmcdrm","xbmcwsgi"]:
        try:
            import sys as _sys
            _sys.modules[_name] = _kodi_shim
        except Exception:
            pass
except Exception as _e:
    print("Warning: failed to import kodi_shim:", _e)
# --- end injected mapping ---

# --- kodi shim mapping injected by assistant ---
try:
    from yacoub.lib import kodi_shim as _kodi_shim
    for _name in ["xbmc","xbmcaddon","xbmcvfs","xbmcplugin","xbmcgui","xbmcdrm","xbmcwsgi"]:
        try:
            import sys as _sys
            _sys.modules[_name] = _kodi_shim
        except Exception:
            pass
except Exception as _e:
    print("Warning: failed to import kodi_shim:", _e)
# --- end injected mapping ---

#!/usr/bin/env python3
"""
Robust headless wrapper (idempotent).
Maps many Kodi modules to the included kodi_mock then imports yacoub.core
and attempts to run detected run_* functions.
"""
import sys, os, traceback

# ensure repo root on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Try to import kodi_mock and map many common Kodi module names to it
mapped_names = [
    "xbmc", "xbmcaddon", "xbmcvfs", "xbmcplugin", "xbmcgui",
    "xbmcdrm", "xbmcwsgi", "xbmcjson", "xbmcutils"
]
try:
    from yacoub.lib import kodi_mock
    for name in mapped_names:
        try:
            # assign the mock module object for each of the names
            sys.modules[name] = kodi_mock
        except Exception:
            pass
except Exception as e:
    print("Warning: failed to import yacoub.lib.kodi_mock:", e)
    traceback.print_exc()

# Now import package core (this will use relative imports correctly)
try:
    from . import core
except Exception as e:
    print("Failed to import yacoub.core (relative imports):", e)
    traceback.print_exc()
    raise

def safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except TypeError:
        # try positional
        try:
            return fn(*args)
        except Exception as e:
            print("Call failed (positional):", e)
            traceback.print_exc()
            return None
    except Exception as e:
        print("Call raised exception:", e)
        traceback.print_exc()
        return None

def run_all():
    # auto-detect run_ functions in core
    runs = [n for n in dir(core) if n.lower().startswith("run_")]
    print("Detected run_ functions in core:", runs, flush=True)
    tests = [
        ("SubDL", getattr(core, "run_subdl_search", None)),
        ("OpenSubtitles", getattr(core, "run_opensubtitles_search", None)),
        ("SubSource", getattr(core, "run_subsource_search", None)),
    ]
    for name, fn in tests:
        print("=== Running:", name, "===", flush=True)
        if not callable(fn):
            print("Function for", name, "not found in core (skipping).")
            continue
        # conservative call attempts
        res = None
        res = safe_call(fn, title="Example Show", season=1, episode=1)
        if res is None:
            res = safe_call(fn, "Example Show", 1, 1)
        if res is None:
            res = safe_call(fn)
        print("Result for", name, ":", repr(res), flush=True)

if __name__ == "__main__":
    run_all()
