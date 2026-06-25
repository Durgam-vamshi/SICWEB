import os
from bs4 import BeautifulSoup

def process_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all the service row containers
    # They have classes like "border-t border-b border-brand-navy/20 grid grid-cols-1 lg:grid-cols-2"
    # Actually let's find all divs that have "grid-cols-1 lg:grid-cols-2" and contain the columns
    rows = soup.select('div.grid-cols-1.lg\:grid-cols-2')
    
    modified = False
    
    # Filter rows that look like our service rows (they have exactly two columns inside usually)
    service_rows = []
    for row in rows:
        # Check if it has the left and right column structure
        cols = row.find_all('div', class_=lambda c: c and 'flex-col' in c, recursive=False)
        if len(cols) == 2:
            service_rows.append(row)
            
    print(f"Found {len(service_rows)} service rows in {filepath}")
    
    for idx, row in enumerate(service_rows):
        left_col = row.find_all('div', recursive=False)[0]
        right_col = row.find_all('div', recursive=False)[1]
        
        # Extract title content
        title_content = None
        # the title is usually the first div in left_col that doesn't have an img
        for div in left_col.find_all('div', recursive=False):
            if not div.find('img'):
                title_content = div
                break
                
        # Extract bullet list
        bullet_list = None
        for div in right_col.find_all('div', recursive=False):
            if not div.find('img'):
                bullet_list = div
                break
                
        # Extract first image found in either column
        img_src = None
        img_tag = left_col.find('img')
        if not img_tag:
            img_tag = right_col.find('img')
            
        if not title_content or not bullet_list or not img_tag:
            print("Could not find required elements in row, skipping.")
            continue
            
        # Build the new Text side
        text_side = soup.new_tag('div')
        # Alternating logic:
        text_is_left = (idx % 2 == 0)
        
        border_class = "lg:border-r border-brand-navy/20" if text_is_left else "lg:border-l border-brand-navy/20"
        text_side['class'] = f"p-8 lg:p-16 flex flex-col justify-center border-b lg:border-b-0 {border_class}"
        
        # append title and list
        text_side.append(title_content)
        
        # add margin to bullet list
        if 'mt-8' not in bullet_list.get('class', []):
            existing_classes = bullet_list.get('class', [])
            bullet_list['class'] = existing_classes + ['mt-10']
        text_side.append(bullet_list)
        
        # Build the new Image side
        img_side = soup.new_tag('div')
        img_side['class'] = "overflow-hidden"
        new_img = soup.new_tag('img')
        new_img['src'] = img_tag['src']
        new_img['class'] = "w-full h-full object-cover min-h-[400px] grayscale hover:grayscale-0 transition-all duration-700"
        img_side.append(new_img)
        
        # Clear the row and append new sides
        row.clear()
        
        if text_is_left:
            row.append(text_side)
            row.append(img_side)
        else:
            # We want the text to be on the right visually in desktop
            # But in DOM, for mobile, we usually want Text on top, then Image.
            # So DOM order: Text, then Image, but on desktop we reverse row!
            # Or we can just put Image first in DOM if we want Image on left.
            # But if mobile should have text first, we can use flex-col-reverse or order classes.
            # The row is `grid grid-cols-1 lg:grid-cols-2`.
            # If we just put img_side first, on mobile the image will be ABOVE the text.
            # That's actually fine for zigzag! It gives a nice break.
            row.append(img_side)
            row.append(text_side)
            
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")

for filename in os.listdir('.'):
    if filename.startswith('services-') and filename.endswith('.html'):
        process_file(filename)
