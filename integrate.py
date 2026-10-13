#!/usr/bin/env python3
import re
from pathlib import Path

repo = Path.home() / 'blog-repo'
html = (repo / 'index.html').read_text(encoding='utf-8')

# --- 1. Tambah 3 kartu ke post-list (sebelum </ul> post-list) ---
new_cards = """  <li class="post-card" data-cat="ai">
    <span class="cat-badge cat-ai">AI</span>
    <h2>AI untuk Social Media: Konten Otomatis yang Engage</h2>
    <p>AI bisa bantu generate ide konten, tulis caption, dan buat kalender konten otomatis untuk media sosial.</p>
    <span class="meta">11 Oktober 2026 &middot; 6 menit baca</span>
    <p><button onclick="buka(44)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
  </li>
  <li class="post-card" data-cat="teknologi">
    <span class="cat-badge cat-teknologi">Teknologi</span>
    <h2>Cara Pakai ADB di Termux: Debug Android dari Terminal</h2>
    <p>ADB (Android Debug Bridge) bisa jalan di Termux, buat debug HP lain, install app, dan pull file tanpa kabel.</p>
    <span class="meta">11 Oktober 2026 &middot; 7 menit baca</span>
    <p><button onclick="buka(45)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
  </li>
  <li class="post-card" data-cat="penghasilan">
    <span class="cat-badge cat-penghasilan">Penghasilan Online</span>
    <h2>SEO untuk Pemula: Rangking di Google Tanpa Iklan</h2>
    <p>Dasar SEO yang bisa langsung dipakai: keyword research, on-page, off-page, dan technical SEO untuk traffic gratis.</p>
    <span class="meta">11 Oktober 2026 &middot; 8 menit baca</span>
    <p><button onclick="buka(46)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
  </li>
"""

# Find the </ul> that closes post-list (the one before pagination)
# The post-list ends with </ul> followed by blank line and pagination div
pattern = r'(</ul>\n\n<div class="pagination")'
match = re.search(pattern, html)
if not match:
    print("ERROR: Could not find post-list closing </ul>")
    exit(1)

html = html[:match.start()] + new_cards + '</ul>\n\n<div class="pagination"' + html[match.end():]

# --- 2. Tambah 3 isi artikel sebelum <footer class="site"> ---
articles_html = ""
for art_file in ['artikel-a44.html', 'artikel-a45.html', 'artikel-a46.html']:
    content = (repo / art_file).read_text(encoding='utf-8')
    articles_html += content + "\n"

# Scan korupsi CJK/Cyrillic di articles_html
bad = set(re.findall(r'[\u4e00-\u9fff\u0400-\u04ff]', articles_html))
if bad:
    print(f"ERROR: Korupsi karakter: {bad}")
    exit(1)

# Insert before <footer class="site">
footer_match = re.search(r'<footer class="site">', html)
if not footer_match:
    print("ERROR: Could not find <footer class='site'>")
    exit(1)

html = html[:footer_match.start()] + articles_html + html[footer_match.start():]

# --- 3. Verifikasi tidak ada duplikat ---
cards = re.findall(r'<li class="post-card"', html)
articles = re.findall(r'<article class="post" id="a\d+">', html)
print(f"Kartu: {len(cards)}, Artikel: {len(articles)}")
if len(cards) != len(articles):
    print("WARNING: Jumlah kartu dan artikel tidak sama!")

# --- 4. Write index.html ---
(repo / 'index.html').write_text(html, encoding='utf-8')
print("index.html updated")

# --- 5. Update sitemap.xml ---
sitemap = (repo / 'sitemap.xml').read_text(encoding='utf-8')

new_urls = """  <url>
    <loc>https://asmady.github.io/#a44</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://asmady.github.io/#a45</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://asmady.github.io/#a46</loc>
    <lastmod>2026-10-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""

# Insert before </urlset>
sitemap = sitemap.replace('</urlset>', new_urls + '</urlset>')
(repo / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
print("sitemap.xml updated")

# --- 6. Final verification ---
html_final = (repo / 'index.html').read_text(encoding='utf-8')
# Check for duplicate article IDs
from collections import Counter
art_ids = re.findall(r'<article class="post" id="a(\d+)">', html_final)
dupes = [item for item, count in Counter(art_ids).items() if count > 1]
if dupes:
    print(f"ERROR: Duplikat artikel: {dupes}")
else:
    print("Tidak ada duplikat artikel")

# Check for CJK/Cyrillic in final file
bad_final = set(re.findall(r'[\u4e00-\u9fff\u0400-\u04ff]', html_final))
if bad_final:
    print(f"ERROR: Korupsi di index.html: {bad_final}")
else:
    print("index.html bersih dari CJK/Cyrillic")

# Word count for each article
for art_file in ['artikel-a44.html', 'artikel-a45.html', 'artikel-a46.html']:
    content = (repo / art_file).read_text(encoding='utf-8')
    text_only = re.sub(r'<[^>]+>', '', content)
    words = len(text_only.split())
    print(f"{art_file}: {words} kata")

print("\nDONE - Siap commit dan push")