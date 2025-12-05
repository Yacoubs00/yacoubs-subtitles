# -*- coding: utf-8 -*-

import importlib
from yacoub.lib import utils

__all = utils.get_all_relative_entries(__file__)
__display_names = {
    'opensubtitles': 'OpenSubtitles',
    'subdl': 'SubDL',
    'subsource': 'SubSource'
}

def __set_fn_if_missing(service, fn_name, fn):
    if not getattr(service, fn_name, None):
        setattr(service, fn_name, fn)

services = {}
for service_name in __all:
    # Skip if not in display names (addic7ed and bsplayer removed)
    if service_name not in __display_names:
        continue
        
    try:
        service = services[service_name] = importlib.import_module('yacoub.services.%s' % service_name)

        service.context = utils.DictAsObject({})
        service.display_name = __display_names[service_name]

        __set_fn_if_missing(service, 'build_auth_request', lambda _, __: None)

        assert service.build_search_requests
        assert service.parse_search_response
        assert service.build_download_request
        
        # Log successful load
        print(f"✓ Loaded provider: {service_name} ({__display_names[service_name]})")
    except Exception as e:
        # Provider failed to load, log the error
        import traceback
        print(f"✗ Failed to load provider {service_name}: {e}")
        print(traceback.format_exc())
        pass
