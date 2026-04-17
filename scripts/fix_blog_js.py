import json

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts_data = f.read()

blog_js = f"""
// Blog SPA Logic
const blogPosts = {posts_data};

function initBlog() {{
    handleHashChange();
    window.addEventListener('hashchange', handleHashChange);
}}

function handleHashChange() {{
    const hash = window.location.hash.substring(1);
    if (hash && hash.startsWith('post-')) {{
        const postId = hash.replace('post-', '');
        const post = blogPosts.find(p => p.id === postId);
        if (post) {{
            renderPost(post);
            return;
        }}
    }}
    // Default: render list
    renderList();
}}

function renderList() {{
    const listContainer = document.getElementById('blog-list');
    const postContainer = document.getElementById('blog-post');
    const heroTitle = document.getElementById('blog-hero-title');
    
    // UI toggles
    listContainer.style.display = 'grid';
    postContainer.style.display = 'none';
    if(heroTitle) heroTitle.innerHTML = 'Blog <span class="text-gradient">Cynor</span>';
    
    // Clear and populate grid
    listContainer.innerHTML = '';
    
    blogPosts.forEach((post, i) => {{
        const delayClass = `delay-${{(i % 3) + 1}}`;
        const cardHTML = `
        <div class="card card--animated reveal ${{delayClass}}" style="display: flex; flex-direction: column; padding: 0; overflow: hidden; cursor:pointer;" onclick="window.location.hash='post-${{post.id}}'">
          <img src="${{post.imagen}}" alt="${{post.titulo}}" style="width: 100%; height: 200px; object-fit: cover;">
          <div style="padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1;">
            <div style="font-size: 0.8rem; color: var(--color-violet); font-family: 'Orbitron', monospace; margin-bottom: 0.5rem;">${{post.categoria}} &bull; ${{post.fecha}}</div>
            <h3 style="font-family: 'DM Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; line-height: 1.4;">${{post.titulo}}</h3>
            <p class="card__text" style="flex-grow: 1; margin-bottom: 1.5rem; font-size: 0.95rem;">${{post.resumen}}</p>
            <button class="btn btn--secondary" style="width: 100%; border: 1px solid rgba(255,255,255,0.1);">Leer artículo</button>
          </div>
        </div>
        `;
        listContainer.insertAdjacentHTML('beforeend', cardHTML);
    }});
}}

function renderPost(post) {{
    const listContainer = document.getElementById('blog-list');
    const postContainer = document.getElementById('blog-post');
    const heroTitle = document.getElementById('blog-hero-title');
    
    // Build post HTML
    // A nice back button
    const html = `
        <button class="btn btn--secondary" style="margin-bottom: 2rem; padding: 10px 20px; font-size: 0.9rem;" onclick="window.location.hash=''">← Volver al Blog</button>
        <img src="${{post.imagen}}" style="width: 100%; height: auto; max-height: 400px; object-fit: cover; border-radius: var(--radius-lg); margin-bottom: 2rem;">
        <div style="color: var(--color-violet); font-family: 'Orbitron', monospace; margin-bottom: 1rem;">${{post.categoria}} &bull; ${{post.fecha}}</div>
        <h1 style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; margin-bottom: 2rem; line-height: 1.2;">${{post.titulo}}</h1>
        <div style="line-height: 1.8; font-size: 1.1rem; color: var(--text-secondary);">
            ${{post.contenido}}
        </div>
    `;
    
    postContainer.innerHTML = html;
    
    // UI toggles
    listContainer.style.display = 'none';
    postContainer.style.display = 'block';
    
    // Optional: Update hero
    if(heroTitle) heroTitle.innerHTML = `<span style="font-size: 1.5rem; opacity: 0.8;">Blog Cynor</span>`;
    
    // Scroll to top
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// Start
document.addEventListener('DOMContentLoaded', initBlog);
"""

with open('js/blog.js', 'w', encoding='utf-8') as f:
    f.write(blog_js)

print("Fixed js/blog.js to include data directly, avoiding fetch CORS issues")
