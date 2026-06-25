import glob
import re

html_files = glob.glob("*.html")
for f in html_files:
    if f == 'index.html':
        continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Very robust regex
    new_content, count = re.subn(
        r'(<span[^>]*dropdown-trigger[^>]*>)\s*Services\s*(<span)', 
        r'\g<1>Industries\g<2>', 
        content,
        flags=re.IGNORECASE
    )
    
    if count > 0:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Replaced in {f} ({count} times)')
    else:
        # One more try for other variations
        new_content2, count2 = re.subn(
            r'Services\s*(<span[^>]*>expand_more)',
            r'Industries\g<1>',
            content,
            flags=re.IGNORECASE
        )
        if count2 > 0:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content2)
            print(f'Replaced in {f} ({count2} times using fallback)')
