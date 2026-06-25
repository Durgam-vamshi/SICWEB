import os
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
import re

def download_wikimedia_image(query, filename):
    print(f"Searching for '{query}'...")
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=5&pithumbsize=800"
    
    headers_api = {'User-Agent': 'CoolBot/1.0 (coolbot@example.com)'}
    headers_img = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers_api)
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            thumbnail = page_data.get('thumbnail')
            if thumbnail:
                img_url = thumbnail['source']
                if img_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"Downloading {img_url} to {filename}")
                    
                    img_req = urllib.request.Request(img_url, headers=headers_img)
                    with urllib.request.urlopen(img_req) as response, open(filename, 'wb') as out_file:
                        out_file.write(response.read())
                    return f"other_assets/dynamic_images/{os.path.basename(filename)}"
                    
        print(f"No suitable image found for '{query}'")
        return None
    except Exception as e:
        print(f"Error fetching '{query}': {e}")
        return None

os.makedirs('other_assets/dynamic_images', exist_ok=True)

def process_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    rows = soup.find_all('div', class_=lambda c: c and 'grid' in c and 'lg:grid-cols-2' in c)
    
    for row in rows:
        title_h4 = row.find('h4', class_=lambda c: c and 'text-2xl' in c)
        if not title_h4:
            continue
            
        title = title_h4.get_text(strip=True)
        img = row.find('img')
        
        if img:
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title).lower()
            filename = f"other_assets/dynamic_images/{safe_title}.jpg"
            
            if not os.path.exists(filename):
                context = filepath.split('-')[1].replace('.html', '')
                search_query = f"{context} {title} professional"
                
                downloaded_path = download_wikimedia_image(search_query, filename)
                if not downloaded_path:
                    downloaded_path = download_wikimedia_image(f"{context} business", filename)
            else:
                downloaded_path = f"other_assets/dynamic_images/{os.path.basename(filename)}"
                
            if downloaded_path and img.get('src') != downloaded_path:
                img['src'] = downloaded_path
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")

for filename in os.listdir('.'):
    if filename.startswith('services-') and filename.endswith('.html'):
        process_file(filename)
