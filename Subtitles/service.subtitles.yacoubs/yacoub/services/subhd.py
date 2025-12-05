# -*- coding: utf-8 -*-

display_name = "SubHD"

def build_search_requests(core, service_name, meta):
    """Search SubHD"""
    query = meta.tvshow if meta.is_tvshow else meta.title
    
    url = "https://subhd.tv/search/" + core.utils.quote_plus(query)
    
    return [{
        'method': 'GET',
        'url': url,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }]

def parse_search_response(core, service_name, meta, response):
    """Parse SubHD HTML response"""
    try:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(response.text, 'html.parser')
        service = core.services[service_name]
        results = []
        
        # Find subtitle entries
        entries = soup.find_all('div', class_='media')
        if not entries:
            entries = soup.find_all('tr')
        
        for entry in entries[:100]:
            try:
                # Extract info
                title_elem = entry.find('a', class_='title')
                if not title_elem:
                    title_elem = entry.find('a')
                
                if not title_elem:
                    continue
                
                name = title_elem.get_text().strip()
                link = title_elem.get('href', '')
                
                if not link.startswith('http'):
                    link = f"https://subhd.tv{link}"
                
                # Get language (default English)
                lang = 'English'
                lang_elem = entry.find('span', class_='language')
                if lang_elem:
                    lang = lang_elem.get_text().strip()
                
                results.append({
                    'service_name': service_name,
                    'service': service.display_name,
                    'lang': lang.capitalize(),
                    'name': name[:80],
                    'rating': 0,
                    'lang_code': 'en',
                    'sync': 'false',
                    'impaired': 'false',
                    'color': 'blue',
                    'action_args': {
                        'url': link,
                        'lang': lang.capitalize(),
                        'filename': name[:80]
                    }
                })
            except:
                continue
        
        return results
        
    except Exception as e:
        core.logger.error(f'{service_name} - {e}')
        return []

def build_download_request(core, service_name, args):
    """Build SubHD download request"""
    return {
        'method': 'GET',
        'url': args['url'],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'stream': True
    }
