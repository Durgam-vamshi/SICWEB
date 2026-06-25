import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

os.makedirs('other_assets/dynamic_images', exist_ok=True)

def download_pollination_image(prompt, filename):
    print(f"Generating image for '{prompt}'...")
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=800&height=600&nologo=true"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
        return f"other_assets/dynamic_images/{os.path.basename(filename)}"
    except Exception as e:
        print(f"Error fetching '{prompt}': {e}")
        return None

def process_file(filepath):
    print(f"\nProcessing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    rows = soup.find_all('div', class_=lambda c: c and 'grid' in c and 'lg:grid-cols-2' in c)
    context = filepath.split('-')[1].replace('.html', '')
    
    for idx, row in enumerate(rows):
        title_h4 = row.find('h4', class_=lambda c: c and 'text-2xl' in c)
        if not title_h4:
            continue
            
        title = title_h4.get_text(strip=True)
        img = row.find('img')
        
        if img:
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title).lower()
            # appending context and idx to avoid cache if needed, but safe_title is good
            filename = f"other_assets/dynamic_images/{context}_{safe_title}.jpg"
            
            prompt = f"Professional corporate photography representing {title} in the {context} sector, realistic business environment, highly detailed, high quality"
            
            # Re-download everything to ensure variety and quality
            downloaded_path = download_pollination_image(prompt, filename)
            
            if downloaded_path:
                img['src'] = downloaded_path
                modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")

for filename in os.listdir('.'):
    if filename.startswith('services-') and filename.endswith('.html'):
        process_file(filename)
