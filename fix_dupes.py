#!/usr/bin/env python3
import re
from pathlib import Path

repo = Path.home() / 'blog-repo'
html = (repo / 'index.html').read_text(encoding='utf-8')

# Hapus artikel duplikat a14, a15, a16 yang ada di sekitar baris 2115-2118
# Pattern: <article class="post" id="a14">...</article> yang duplikat
# Kita perlu menghapus yang kedua (yang ada setelah a13)

# Cari semua artikel a14, a15, a16
pattern_a14 = r'<article class="post" id="a14">.*?</article>'
pattern_a15 = r'<article class="post" id="a15">.*?</article>'
pattern_a16 = r'<article class="post" id="a16">.*?</article>'

matches_a14 = list(re.finditer(pattern_a14, html, re.DOTALL))
matches_a15 = list(re.finditer(pattern_a15, html, re.DOTALL))
matches_a16 = list(re.finditer(pattern_a16, html, re.DOTALL))

print(f"a14 ditemukan: {len(matches_a14)}x")
print(f"a15 ditemukan: {len(matches_a15)}x")
print(f"a16 ditemukan: {len(matches_a16)}x")

# Hapus yang kedua (duplikat) untuk masing-masing
# Kita hapus dari belakang agar index tidak bergeser
to_remove = []
if len(matches_a14) > 1:
    to_remove.append(matches_a14[-1])
if len(matches_a15) > 1:
    to_remove.append(matches_a15[-1])
if len(matches_a16) > 1:
    to_remove.append(matches_a16[-1])

# Urutkan dari belakang ke depan
to_remove.sort(key=lambda m: m.start(), reverse=True)

for match in to_remove:
    print(f"Menghapus duplikat di posisi {match.start()}-{match.end()}")
    html = html[:match.start()] + html[match.end():]

# Verifikasi
from collections import Counter
art_ids = re.findall(r'<article class="post" id="a(\d+)">', html)
dupes = [item for item, count in Counter(art_ids).items() if count > 1]
if dupes:
    print(f"MASIH ADA DUPLIKAT: {dupes}")
else:
    print("Tidak ada duplikat artikel")

# Cek kartu vs artikel
cards = re.findall(r'<li class="post-card"', html)
articles = re.findall(r'<article class="post" id="a\d+">', html)
print(f"Kartu: {len(cards)}, Artikel: {len(articles)}")

(repo / 'index.html').write_text(html, encoding='utf-8')
print("index.html diperbaiki")