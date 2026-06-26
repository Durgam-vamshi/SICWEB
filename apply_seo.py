import os
import glob
from bs4 import BeautifulSoup

def process_html_file(filepath):
    print(f"Processing {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    filename = os.path.basename(filepath)

    page_data = {
        'index.html': {
            'title': 'Sapphire Intel Consulting | Strategic Intelligence & Business Consulting',
            'desc': 'Sapphire Intel Consulting provides strategic intelligence, business consulting, AI automation, market research, growth advisory, and transformation solutions for healthcare, pharmaceutical, D2C, real estate, and enterprise businesses.'
        },
        'about.html': {
            'title': 'About Us | Sapphire Intel Consulting',
            'desc': 'Learn about Sapphire Intel Consulting, a strategic advisory firm helping businesses scale through intelligence-driven consulting and transformation.'
        },
        'contact.html': {
            'title': 'Contact Us | Sapphire Intel Consulting Hyderabad',
            'desc': 'Contact Sapphire Intel Consulting for strategic advisory, business consulting, market intelligence, AI automation, and growth consulting services.'
        },
        'services-healthcare.html': {
            'title': 'Healthcare Consulting Services | Sapphire Intel Consulting',
            'desc': 'Healthcare consulting services focused on operational excellence, health-tech strategy, compliance, and hospital transformation.'
        },
        'services-pharma.html': {
            'title': 'Pharmaceutical Consulting Services | Sapphire Intel Consulting',
            'desc': 'Pharmaceutical consulting solutions focused on regulatory affairs, pipeline strategy, and commercial strategy.'
        },
        'services-real-estate.html': {
            'title': 'Real Estate Consulting Services | Sapphire Intel Consulting',
            'desc': 'Real estate business consulting services including AI-enabled advisory, operational excellence, and project strategy.'
        },
        'services-d2c.html': {
            'title': 'D2C Growth Consulting Services | Sapphire Intel Consulting',
            'desc': 'D2C brand growth consulting solutions for omnichannel growth, scalable operations, and brand positioning.'
        },
        'casestudies_combined.html': {
            'title': 'Case Studies | Sapphire Intel Consulting',
            'desc': 'Explore our transformative case studies across healthcare, pharmaceutical, D2C, and real estate sectors.'
        },
        'insights.html': {
            'title': 'Business Insights & Thought Leadership | Sapphire Intel Consulting',
            'desc': 'Stay ahead with perspectives from Sapphire Intel Consulting on strategy, industry trends, and growth best practices.'
        },
        'services-general.html': {
            'title': 'General Business Consulting Services | Sapphire Intel Consulting',
            'desc': 'General business consulting focused on corporate strategy, transformation, and organizational design.'
        },
        'services.html': {
            'title': 'Our Industries | Sapphire Intel Consulting',
            'desc': 'Explore our specialized consulting services across healthcare, pharmaceutical, real estate, and D2C industries.'
        }
    }

    data = page_data.get(filename, {
        'title': f'{filename.replace(".html", "").title()} | Sapphire Intel Consulting',
        'desc': 'Sapphire Intel Consulting provides strategic advisory and business transformation solutions.'
    })

    head = soup.find('head')
    if head:
        for tag in head.find_all(['title', 'meta', 'link']):
            if tag.name == 'title':
                tag.decompose()
            elif tag.name == 'link' and tag.get('rel') == ['canonical']:
                tag.decompose()
            elif tag.name == 'link' and tag.get('rel') == ['icon']:
                tag.decompose()
            elif tag.name == 'meta' and tag.get('name') in ['description', 'twitter:card', 'twitter:title', 'twitter:description']:
                tag.decompose()
            elif tag.name == 'meta' and tag.get('property') in ['og:title', 'og:description', 'og:url', 'og:type']:
                tag.decompose()

        new_title = soup.new_tag('title')
        new_title.string = data['title']
        head.append(new_title)

        meta_desc = soup.new_tag('meta', attrs={'name': 'description', 'content': data['desc']})
        head.append(meta_desc)

        canonical_url = f'https://sapphireintelconsulting.com/{"" if filename == "index.html" else filename}'
        canonical = soup.new_tag('link', rel='canonical', href=canonical_url)
        head.append(canonical)

        favicon = soup.new_tag('link', rel='icon', href='/favicon.ico', type='image/x-icon')
        head.append(favicon)

        og_title = soup.new_tag('meta', property='og:title', content=data['title'])
        og_desc = soup.new_tag('meta', property='og:description', content=data['desc'])
        og_url = soup.new_tag('meta', property='og:url', content=canonical_url)
        og_type = soup.new_tag('meta', property='og:type', content='website')
        head.extend([og_title, og_desc, og_url, og_type])

        tw_card = soup.new_tag('meta', attrs={'name': 'twitter:card', 'content': 'summary_large_image'})
        tw_title = soup.new_tag('meta', attrs={'name': 'twitter:title', 'content': data['title']})
        tw_desc = soup.new_tag('meta', attrs={'name': 'twitter:description', 'content': data['desc']})
        head.extend([tw_card, tw_title, tw_desc])

    if filename == 'index.html':
        for script in soup.find_all('script', type='application/ld+json'):
            script.decompose()
        schema_script = soup.new_tag('script', type='application/ld+json')
        schema_script.string = '''
{
  "@context":"https://schema.org",
  "@type":"Organization",
  "name":"Sapphire Intel Consulting",
  "url":"https://sapphireintelconsulting.com",
  "logo":"https://sapphireintelconsulting.com/logo.png"
}
'''
        head.append(schema_script)

    for idx, img in enumerate(soup.find_all('img')):
        if not img.get('alt') or len(img.get('alt', '')) < 5:
            img_src = img.get('src', '').lower()
            if 'healthcare' in img_src or 'healthcare' in filename:
                alt_text = "Healthcare consulting services by Sapphire Intel Consulting"
            elif 'pharma' in img_src or 'pharma' in filename:
                alt_text = "Pharmaceutical consulting solutions by Sapphire Intel Consulting"
            elif 'real-estate' in img_src or 'real_estate' in filename or 'real' in filename:
                alt_text = "Real estate business consulting services by Sapphire Intel Consulting"
            elif 'd2c' in img_src or 'd2c' in filename:
                alt_text = "D2C brand growth consulting solutions by Sapphire Intel Consulting"
            else:
                alt_text = "Business transformation consulting experts at Sapphire Intel Consulting"
            img['alt'] = alt_text
        
        if idx > 1 and not img.get('loading'):
            img['loading'] = 'lazy'

    h1_tags = soup.find_all('h1')
    for i, h1 in enumerate(h1_tags):
        if i > 0:
            h1.name = 'h2'

    navs = soup.find_all('nav')
    for nav in navs:
        if 'navbar' in nav.get('class', []) and not nav.find_parent('header'):
            header = soup.new_tag('header')
            nav.wrap(header)

    if filename == 'index.html':
        footer = soup.find('footer')
        if footer:
            seo_section = soup.new_tag('section', attrs={'class': 'bg-[#121317] text-gray-400 py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto'})
            seo_html = """
<div class="border-t border-gray-800 pt-12">
    <h2 class="text-2xl font-serif text-white mb-6">About Sapphire Intel Consulting</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-sm leading-relaxed">
        <p>
            Sapphire Intel Consulting is a strategic advisory and business consulting firm helping enterprises achieve sustainable growth through intelligence-driven decision making, operational transformation, AI automation, market research, and executive consulting.
        </p>
        <p>
            We work with healthcare organizations, pharmaceutical companies, real estate businesses, D2C brands, and enterprises to optimize operations, improve efficiency, identify growth opportunities, and implement scalable business transformation strategies.
        </p>
        <p>
            Our consulting expertise includes mergers and acquisitions advisory, due diligence, market intelligence, automation strategy, branding strategy, go-to-market planning, executive consulting, and business growth consulting.
        </p>
    </div>
</div>
"""
            seo_section.append(BeautifulSoup(seo_html, 'html.parser'))
            
            existing_seo = soup.find('h2', string='About Sapphire Intel Consulting')
            if not existing_seo:
                footer.insert_before(seo_section)

    for a in soup.find_all('a'):
        if a.get('href') == '':
            a['href'] = '#'

    with open(filepath, 'w', encoding='utf-8') as f:
        # Use str(soup) instead of prettify to avoid breaking tailwind classes / spacing
        # Ensure we write HTML5 DOCTYPE correctly since bs4 sometimes converts it weirdly
        f.write(str(soup).replace('<!DOCTYPE html>', '<!DOCTYPE html>\n', 1))

if __name__ == '__main__':
    for filepath in glob.glob('*.html'):
        process_html_file(filepath)
