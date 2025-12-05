# -*- coding: utf-8 -*-

display_name = "YIFY"

def build_search_requests(core, service_name, meta):
    """Search YIFY subtitles using IMDB ID"""
    if meta.is_tvshow:
        return []  # YIFY is movies only
    
    if not meta.imdb_id:
        return []
    
    # Use yts-subs.com
    url = f"https://yts-subs.com/movie-imdb/{meta.imdb_id}"
    
    return [{
        'method': 'GET',
        'url': url,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }]

def parse_search_response(core, service_name, meta, response):
    """Parse YIFY HTML response"""
    try:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(response.text, 'html.parser')
        service = core.services[service_name]
        results = []
        
        # Find subtitle table
        table = soup.find('table', class_='other-subs')
        if not table:
            return []
        
        # Get all rows
        rows = table.find_all('tr')[1:]  # Skip header
        
        for row in rows[:100]:  # Limit to 30
            try:
                cells = row.find_all('td')
                if len(cells) < 5:
                    continue
                
                # Extract data: rating, language, release, uploader, download
                rating_cell = cells[0]
                lang_cell = cells[1]
                release_cell = cells[2]
                download_cell = cells[4]
                
                # Get language
                lang = lang_cell.get_text().strip()
                
                # Filter by language
                if not any(l.lower() in lang.lower() for l in ['english', 'eng']):
                    continue
                
                # Get subtitle name
                release_link = release_cell.find('a')
                if release_link:
                    name = release_link.get_text().strip()
                else:
                    name = release_cell.get_text().strip()
                
                # Get download link
                download_link = download_cell.find('a', href=True)
                if not download_link:
                    continue
                
                download_url = download_link['href']
                if not download_url.startswith('http'):
                    download_url = f"https://yts-subs.com{download_url}"
                
                # Get rating
                rating_text = rating_cell.get_text().strip()
                try:
                    rating = int(rating_text) if rating_text.isdigit() else 0
                except:
                    rating = 0
                
                results.append({
                    'service_name': service_name,
                    'service': service.display_name,
                    'lang': 'English',
                    'name': name[:80],
                    'rating': rating,
                    'lang_code': 'en',
                    'sync': 'true' if meta.filename_without_ext in name else 'false',
                    'impaired': 'false',
                    'color': 'yellow',
                    'action_args': {
                        'url': download_url,
                        'lang': 'English',
                        'filename': name[:80]
                    }
                })
            except Exception as e:
                continue
        
        return results
        
    except Exception as e:
        core.logger.error(f'{service_name} - {e}')
        return []

def build_download_request(core, service_name, args):
    """Build YIFY download request"""
    return {
        'method': 'GET',
        'url': args['url'],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://yts-subs.com/'
        },
        'stream': True
    }
