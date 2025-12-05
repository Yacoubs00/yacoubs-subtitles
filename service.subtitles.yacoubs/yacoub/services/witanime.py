# -*- coding: utf-8 -*-
"""
Witanime - Arabic anime subtitle provider
Website: https://witanime.cam
Focus: Arabic subtitles for anime
"""

def build_search_requests(core, service_name, meta):
    """Build search request for Witanime"""
    
    # Only search for anime/TV shows
    if not meta.is_tvshow:
        core.logger.debug('%s - Skipping non-TV content' % service_name)
        return []
    
    # Search for Arabic subtitles (but still search if user has English selected, as Witanime might have both)
    # Most users will have both Arabic and English selected
    core.logger.debug('%s - Searching for anime subtitles (Arabic focus)' % service_name)
    
    # Search query - anime title
    # URL encode the query
    try:
        from urllib.parse import quote
    except ImportError:
        from urllib import quote as url_quote
        query = url_quote(meta.tvshow)
    else:
        query = quote(meta.tvshow)
    
    # Build search URL
    search_url = f"https://witanime.cam/?search_param=animes&s={query}"
    
    core.logger.debug('%s - Searching for: %s' % (service_name, meta.tvshow))
    
    request = {
        'method': 'GET',
        'url': search_url,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Referer': 'https://witanime.cam/'
        }
    }
    
    return [request]

def parse_search_response(core, service_name, meta, response):
    """Parse Witanime search results"""
    
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
        
        # Witanime uses various structures - try multiple selectors
        anime_entries = (
            soup.find_all('div', class_='anime-card-container') or
            soup.find_all('div', class_='anime-card') or
            soup.find_all('article', class_='anime') or
            soup.find_all('div', class_='result-item')
        )
        
        core.logger.debug('%s - Found %d anime entries' % (service_name, len(anime_entries)))
        
        if not anime_entries:
            # If no specific containers, look for any links with "anime" or "episode" in URL
            all_links = soup.find_all('a', href=True)
            anime_entries = [a for a in all_links if 'anime' in a.get('href', '').lower() or 'episode' in a.get('href', '').lower()]
            core.logger.debug('%s - Found %d links with anime/episode' % (service_name, len(anime_entries)))
        
        for entry in anime_entries[:20]:  # Limit to first 20
            try:
                # Get the link
                if entry.name == 'a':
                    link = entry
                    title_elem = entry
                else:
                    link = entry.find('a', href=True)
                    title_elem = entry.find(['h3', 'h2', 'h4', 'span', 'div'], class_=lambda x: x and ('title' in x.lower() or 'name' in x.lower()))
                    if not title_elem:
                        title_elem = entry.find('a')
                
                if not link:
                    continue
                    
                url = link.get('href', '')
                if not url.startswith('http'):
                    url = 'https://witanime.cam' + url
                
                title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
                
                # Create subtitle entry
                subtitle = {
                    'service_name': service_name,
                    'service': service.display_name,
                    'lang': 'Arabic',
                    'name': f"{title} - Arabic Subs",
                    'rating': 0,
                    'lang_code': 'ar',
                    'sync': 'false',
                    'impaired': 'false',
                    'color': 'lightgreen',
                    'action_args': {
                        'url': url,
                        'lang': 'Arabic',
                        'filename': title
                    }
                }
                
                results.append(subtitle)
                
            except Exception as e:
                core.logger.debug('%s - Error parsing entry: %s' % (service_name, str(e)))
                continue
        
        core.logger.debug('%s - Returning %d results' % (service_name, len(results)))
        
    except Exception as exc:
        core.logger.error('%s - Parse error: %s' % (service_name, str(exc)))
        import traceback
        core.logger.error(traceback.format_exc())
    
    return results

def build_download_request(core, service_name, args):
    """Build download request - fetch the episode page to find subtitle link"""
    
    core.logger.debug('%s - Fetching episode page: %s' % (service_name, args['url']))
    
    request = {
        'method': 'GET',
        'url': args['url'],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://witanime.cam/'
        }
    }
    
    return request

def parse_download_response(core, service_name, args, response):
    """Parse episode page to find actual subtitle download link"""
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for subtitle download links
        # Common patterns: .srt, .ass, subtitles/, download-srt/, etc.
        subtitle_links = soup.find_all('a', href=True)
        
        for link in subtitle_links:
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Check if it's a subtitle link
            if any(ext in href.lower() for ext in ['.srt', '.ass', '.ssa', '.sub', 'subtitle', 'تحميل']):
                if not href.startswith('http'):
                    href = 'https://witanime.cam' + href
                
                core.logger.debug('%s - Found subtitle link: %s' % (service_name, href))
                
                return {
                    'method': 'GET',
                    'url': href,
                    'headers': {
                        'User-Agent': 'Mozilla/5.0',
                        'Referer': args['url']
                    },
                    'stream': True
                }
        
        core.logger.error('%s - No subtitle download link found' % service_name)
        
    except Exception as e:
        core.logger.error('%s - Download parse error: %s' % (service_name, str(e)))
    
    return None
