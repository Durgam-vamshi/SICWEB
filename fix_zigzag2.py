import os
from bs4 import BeautifulSoup
import re

def get_page_image(filename):
    if 'healthcare' in filename:
        return 'other_assets/industries_images/healthcare.jpg'
    elif 'pharma' in filename:
        return 'other_assets/industries_images/pharma.jpg'
    elif 'd2c' in filename:
        return 'other_assets/industries_images/d2c.jpg'
    elif 'real-estate' in filename:
        return 'other_assets/industries_images/realestate.jpg'
    else:
        return 'other_assets/generalconsulting.jpg'

def process_file(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    # Match both old layout (grid-cols-12) and new layout (grid-cols-2)
    # Old layout rows have "row-border grid grid-cols-1 lg:grid-cols-12"
    # Or "border-t border-b border-brand-navy/20 grid grid-cols-1 lg:grid-cols-2"
    rows = soup.find_all('div', class_=lambda c: c and 'grid' in c and ('lg:grid-cols-12' in c or 'lg:grid-cols-2' in c))
    
    service_rows = []
    for row in rows:
        cols = row.find_all('div', recursive=False)
        if len(cols) == 2:
            service_rows.append(row)
            
    print(f"Found {len(service_rows)} service rows in {filepath}")
    
    for idx, row in enumerate(service_rows):
        left_col = row.find_all('div', recursive=False)[0]
        right_col = row.find_all('div', recursive=False)[1]
        
        # Check if this is the "zigzag" already applied (p-8 lg:p-16)
        if "lg:p-16" in left_col.get('class', []) or "lg:p-16" in right_col.get('class', []):
            # Already zigzagged!
            print("Already zigzagged")
            # But let's fix the broken image paths if they are broken
            img = row.find('img')
            if img and 'hospital-team.jpg' in img.get('src', '') or 'operations-dashboard.jpg' in img.get('src', ''):
                img['src'] = get_page_image(filepath)
                modified = True
            continue
            
        title_content = None
        bullet_list = None
        
        # Extract title and bullet list based on old or new layout
        if "lg:col-span-4" in left_col.get('class', []):
            # Old layout
            title_content = left_col
            bullet_list = right_col
        else:
            # New layout but not zigzagged yet
            for div in left_col.find_all('div', recursive=False):
                if not div.find('img'):
                    title_content = div
                    break
            for div in right_col.find_all('div', recursive=False):
                if not div.find('img'):
                    bullet_list = div
                    break
                    
        if not title_content or not bullet_list:
            print("Could not find title or list")
            continue
            
        # Clean up title classes from old layout
        if "lg:col-span-4" in title_content.get('class', []):
            classes = title_content.get('class', [])
            title_content['class'] = [c for c in classes if 'lg:col-span-4' not in c and 'pr-8' not in c and 'py-6' not in c]
            
        # Clean up bullet list classes from old layout
        if "lg:col-span-8" in bullet_list.get('class', []):
            classes = bullet_list.get('class', [])
            bullet_list['class'] = [c for c in classes if 'lg:col-span-8' not in c and 'lg:border-l' not in c and 'grid' not in c]

        img_src = get_page_image(filepath)
        
        # Build the new Text side
        text_side = soup.new_tag('div')
        text_is_left = (idx % 2 == 0)
        
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
        
        # Update row classes
        row['class'] = "border-t border-b border-brand-navy/20 grid grid-cols-1 lg:grid-cols-2 bg-white"
        
        row.clear()
        
        if text_is_left:
            row.append(text_side)
            row.append(img_side)
        else:
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
