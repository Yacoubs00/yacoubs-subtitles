# -*- coding: utf-8 -*-
"""
Kitsunekko - Japanese anime subtitle provider
Website: https://kitsunekko.net
Focus: Japanese subtitles for anime
"""

def build_search_requests(core, service_name, meta):
    """Search Kitsunekko for anime Japanese subtitles"""
    
    # Kitsunekko provides Japanese subs for anime
    # We'll search regardless of language selection since it's anime-focused
    
    # Get the title
    title = meta.tvshow if meta.is_tvshow else meta.title
    
    # Kitsunekko directory listing
    url = "https://kitsunekko.net/dirlist.php"
    params = {'dir': 'subtitles/japanese/'}
    
    core.logger.debug('%s - Searching for: %s' % (service_name, title))
    
    return [{
        'method': 'GET',
        'timeout': 10,
        'url': url,
        'params': params,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }]

def parse_search_response(core, service_name, meta, response):
    """Parse Kitsunekko directory listing"""
    
    if response.status_code != 200:
        core.logger.error('%s - HTTP %d' % (service_name, response.status_code))
        return []
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        core.logger.error('%s - BeautifulSoup4 not available' % service_name)
        return []
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        service = core.services[service_name]
        results = []
        
        title = (meta.tvshow if meta.is_tvshow else meta.title).lower()
        # Normalize title for matching
        title_normalized = title.replace(' ', '').replace('-', '').replace('_', '')
        
        core.logger.debug('%s - Looking for directories matching: %s' % (service_name, title))
        
        # Find directory links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # Skip parent directory and non-directory links
            if text == '..' or not text:
                continue
            
            # Normalize link text for matching
            text_normalized = text.lower().replace(' ', '').replace('-', '').replace('_', '')
            
            # Fuzzy match: check if significant portion matches
            if (title_normalized in text_normalized or 
                text_normalized in title_normalized or
                any(word in text_normalized for word in title.split() if len(word) > 3)):
                
                # Found matching anime directory
                dir_url = f"https://kitsunekko.net/dirlist.php?dir=subtitles/japanese/{href}"
                
                core.logger.debug('%s - Found match: %s' % (service_name, text))
                
                results.append({
                    'service_name': service_name,
                    'service': service.display_name,
                    'lang': 'Japanese',
                    'name': f"{text} (Japanese)",
                    'rating': 0,
                    'lang_code': 'ja',
                    'sync': 'false',
                    'impaired': 'false',
                    'color': 'pink',
                    'action_args': {
                        'url': dir_url,
                        'lang': 'Japanese',
                        'filename': text,
                        'directory': href
                    }
                })
        
        core.logger.debug('%s - Found %d matching directories' % (service_name, len(results)))
        return results[:20]  # Limit results
        
    except Exception as e:
        core.logger.error('%s - Parse error: %s' % (service_name, str(e)))
        import traceback
        core.logger.error(traceback.format_exc())
        return []

def build_download_request(core, service_name, args):
    """Build request to get files from anime directory"""
    
    core.logger.debug('%s - Fetching directory: %s' % (service_name, args['url']))
    
    return {
        'method': 'GET',
        'timeout': 10,
        'url': args['url'],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }

def parse_download_response(core, service_name, args, response):
    """Parse anime directory to find subtitle files"""
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for .ass or .srt files
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # Check if it's a subtitle file
            if any(href.endswith(ext) for ext in ['.ass', '.srt', '.ssa', '.sub']):
                file_url = f"https://kitsunekko.net/subtitles/japanese/{args['directory']}/{href}"
                
                core.logger.debug('%s - Found subtitle file: %s' % (service_name, text))
                
                return {
                    'method': 'GET',
                    'url': file_url,
                    'headers': {
                        'User-Agent': 'Mozilla/5.0',
                        'Referer': args['url']
                    },
                    'stream': True
                }
        
        core.logger.error('%s - No subtitle files found in directory' % service_name)
        
    except Exception as e:
        core.logger.error('%s - Download parse error: %s' % (service_name, str(e)))
    
    return None
