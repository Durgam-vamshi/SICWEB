import os
from bs4 import BeautifulSoup
import re

def process_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    rows = soup.find_all('div', class_=lambda c: c and 'grid' in c and ('lg:grid-cols-12' in c or 'lg:grid-cols-2' in c))
    
    service_rows = []
    for row in rows:
        cols = row.find_all('div', recursive=False)
        if len(cols) == 2:
            service_rows.append(row)
            
    valid_idx = 0
    for row in service_rows:
        left_col = row.find_all('div', recursive=False)[0]
        right_col = row.find_all('div', recursive=False)[1]
        
        # We need to extract the title and the list from whatever is in these columns.
        title_content = None
        bullet_list = None
        
        # Find the div containing the text "01", "02", etc.
        for col in [left_col, right_col]:
            for div in col.find_all('div', recursive=False):
                if div.find(string=re.compile(r'0[1-9]')):
                    title_content = div
                elif div.find('div', class_=lambda c: c and 'border-b' in c) or div.find('p', class_=lambda c: c and 'text-lg' in c):
                    # this is likely the bullet list
                    if not div.find('img'):
                        bullet_list = div
                        
        if not title_content or not bullet_list:
            continue
            
        # Clean up classes
        if "lg:col-span-4" in title_content.get('class', []):
            classes = title_content.get('class', [])
            title_content['class'] = [c for c in classes if 'lg:col-span-4' not in c and 'pr-8' not in c and 'py-6' not in c]
            
        if "lg:col-span-8" in bullet_list.get('class', []):
            classes = bullet_list.get('class', [])
            bullet_list['class'] = [c for c in classes if 'lg:col-span-8' not in c and 'lg:border-l' not in c and 'grid' not in c]

        # Extract image if exists, else default
        img_src = 'other_assets/industries_images/healthcare.jpg'
        
        # Build the new Text side
        text_side = soup.new_tag('div')
        text_is_left = (valid_idx % 2 == 0)
        
        border_class = "lg:border-r border-brand-navy/20" if text_is_left else "lg:border-l border-brand-navy/20"
        text_side['class'] = f"p-8 lg:p-16 flex flex-col justify-center border-b lg:border-b-0 {border_class}"
        
        text_side.append(title_content)
        
        if 'mt-10' not in bullet_list.get('class', []):
            existing_classes = bullet_list.get('class', [])
            bullet_list['class'] = existing_classes + ['mt-10']
            
        text_side.append(bullet_list)
        
        # Build the new Image side
        img_side = soup.new_tag('div')
        img_side['class'] = "overflow-hidden flex items-center justify-center bg-gray-100"
        new_img = soup.new_tag('img')
        new_img['src'] = img_src
        new_img['class'] = "w-full h-full object-cover min-h-[400px] grayscale hover:grayscale-0 transition-all duration-700"
        img_side.append(new_img)
        
        row['class'] = "border-t border-b border-brand-navy/20 grid grid-cols-1 lg:grid-cols-2 bg-white"
        row.clear()
        
        if text_is_left:
            row.append(text_side)
            row.append(img_side)
        else:
            row.append(img_side)
            row.append(text_side)
            
        valid_idx += 1
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")

process_file('services-healthcare.html')
