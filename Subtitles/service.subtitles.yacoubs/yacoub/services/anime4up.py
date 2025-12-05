# -*- coding: utf-8 -*-
"""
Anime4up - Arabic anime subtitle provider
Website: https://w1.anime4up.cam
Focus: Arabic subtitles for anime
"""

def build_search_requests(core, service_name, meta):
    """Build search request for Anime4up"""
    
    # Only search for anime/TV shows
    if not meta.is_tvshow:
        return []
    
    # Only search for Arabic subtitles
    lang_ids = core.utils.get_lang_ids(meta.languages, core.kodi.xbmc.ISO_639_1)
    if 'ar' not in lang_ids:
        return []
    
    # Search query - anime title
    query = meta.tvshow if meta.is_tvshow else meta.title
    
    # Build search URL
    search_url = f"https://w1.anime4up.cam/?search_param=animes&s={query}"
    
    request = {
        'method': 'GET',
        'url': search_url,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    return [request]

def parse_search_response(core, service_name, meta, response):
    """Parse Anime4up search results"""
    
    if response.status_code != 200:
        core.logger.error('%s - HTTP %d' % (service_name, response.status_code))
        return []
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        core.logger.error('%s - BeautifulSoup4 not available' % service_name)
        return []
    
    service = core.services[service_name]
    results = []
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find anime entries (adjust selectors based on actual site structure)
        anime_entries = soup.find_all('div', class_='anime-card-container') or \
                       soup.find_all('article', class_='post') or \
                       soup.find_all('div', class_='anime-card')
        
        core.logger.debug('%s - Found %d potential entries' % (service_name, len(anime_entries)))
        
        for entry in anime_entries[:10]:  # Limit to first 10 results
            try:
                # Extract title and link (adjust based on actual HTML)
                title_elem = entry.find('h3') or entry.find('h2') or entry.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = entry.find('a')
                
                if link and 'href' in link.attrs:
                    url = link['href']
                    
                    # Create subtitle entry
                    subtitle = {
                        'service_name': service_name,
                        'service': service,
                        'lang': 'Arabic',
                        'name': title,
                        'rating': '0',
                        'lang_code': 'ar',
                        'sync': False,
                        'impaired': False,
                        'color': 'white',
                        'action_args': {
                            'url': url,
                            'title': title
                        }
                    }
                    
                    results.append(subtitle)
                    
            except Exception as e:
                core.logger.debug('%s - Error parsing entry: %s' % (service_name, str(e)))
                continue
        
        core.logger.info('%s - Found %d subtitles' % (service_name, len(results)))
        
    except Exception as exc:
        core.logger.error('%s - Parse error: %s' % (service_name, str(exc)))
    
    return results

def build_download_request(core, service_name, args):
    """Build download request - needs actual subtitle file URL from detail page"""
    
    # This would need to fetch the detail page and find the subtitle download link
    # For now, return empty as we need to inspect the actual site structure
    
    request = {
        'method': 'GET',
        'url': args['url'],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    return request

def parse_download_response(core, service_name, meta, response):
    """Parse download page to get actual subtitle file"""
    
    # Would need to parse the detail page HTML to find the actual .srt/.ass file link
    # Return empty for now - needs site inspection
    
    return None
