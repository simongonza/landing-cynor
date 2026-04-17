import re
import glob

html_files = glob.glob("*.html")
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean any previously incorrectly added or duplicate links
    # content = content.replace('<a href="blog.html" class="navbar__link">Blog</a>', '')
    
    # If the file does not have the desktop navbar Blog link
    if '<a href="blog.html" class="navbar__link' not in content:
        content = re.sub(r'(<a href="quienes-somos\.html" class="navbar__link"(?: active)?>Quiénes Somos</a>)',
                         r'\1\n        <a href="blog.html" class="navbar__link">Blog</a>', content)
                         
    if 'href="blog.html"' not in content:
        # Extreme fallback
        pass
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Desktop Navbar fixed")
