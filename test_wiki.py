import os
import urllib.request
import urllib.parse
import json

def download_wikimedia_image(query, filename):
    print(f"Searching for '{query}'...")
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=5&pithumbsize=800"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
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
                    urllib.request.urlretrieve(img_url, filename)
                    return True
        print(f"No suitable image found for '{query}'")
        return False
    except Exception as e:
        print(f"Error fetching '{query}': {e}")
        return False

# Ensure folder exists
os.makedirs('other_assets/dynamic_images', exist_ok=True)

# Test search
download_wikimedia_image('hospital surgery', 'other_assets/dynamic_images/test.jpg')
