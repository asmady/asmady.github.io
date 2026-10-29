import re
from pathlib import Path

P = Path('/data/data/com.termux/files/home/blog-repo/index.html')
h = P.read_text(encoding='utf-8')

# Baca artikel dari file
base = Path('/data/data/com.termux/files/home/blog-repo/artikel_baru')
a125 = (base / 'a125.html').read_text(encoding='utf-8').strip()
a126 = (base / 'a126.html').read_text(encoding='utf-8').strip()
a127 = (base / 'a127.html').read_text(encoding='utf-8').strip()

# === SISIPKAN KARTU BARU DI PALING ATAS post-list ===
kartu_125 = '''<li class="post-card" data-cat="ai" data-tag="AI|Video|Tools|Editing">
<span class="cat-badge cat-ai">AI</span>
<h2>AI untuk Video Editing: Edit Video Otomatis dalam Hitungan Menit</h2>
<p>Upload footage mentah, minta AI potong bagian terbaik, tambahkan subtitle, transisi, dan voiceover — semua otomatis dari HP Android.</p>
<span class="meta">20 Oktober 2026 &middot; 6 menit baca</span>
<p><button onclick="buka(125)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
</li>'''

kartu_126 = '''<li class="post-card" data-cat="teknologi" data-tag="Termux|Android|Redis|Database|Server">
<span class="cat-badge cat-teknologi">Teknologi</span>
<h2>Redis di Termux: Database In-Memory untuk Cache dan Queue</h2>
<p>Redis adalah database in-memory super cepat untuk cache, session, queue — bisa jalan di HP Android lewat Termux.</p>
<span class="meta">20 Oktober 2026 &middot; 7 menit baca</span>
<p><button onclick="buka(126)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
</li>'''

kartu_127 = '''<li class="post-card" data-cat="penghasilan" data-tag="Kursus|Online|Bisnis|Monetisasi|Digital Product">
<span class="cat-badge cat-penghasilan">Penghasilan Online</span>
<h2>Kursus Online: Jual Ilmu dan Skill dengan Platform Kursus</h2>
<p>Bikin sekali, jual berkali-kali. Kursus online adalah cara terbaik monetisasi expertise yang scalable — mulai dari HP Android.</p>
<span class="meta">20 Oktober 2026 &middot; 6 menit baca</span>
<p><button onclick="buka(127)" style="background:none;border:none;color:var(--accent-deep);cursor:pointer;font-size:14px;padding:0;font-family:inherit;font-weight:500">Baca artikel &rarr;</button></p>
</li>'''

# Cari baris <ul class="post-list" id="postList">
postlist_marker = '<ul class="post-list" id="postList">\n'
idx = h.find(postlist_marker)
if idx == -1:
    print("ERROR: post-list marker tidak ditemukan")
else:
    insert_pos = idx + len(postlist_marker)
    # Urutan: a127 (terbaru) paling atas, lalu a126, lalu a125
    kartu_block = kartu_127 + '\n' + kartu_126 + '\n' + kartu_125 + '\n'
    h = h[:insert_pos] + kartu_block + h[insert_pos:]
    line_num = h[:insert_pos].count('\n') + 1
    print("Kartu baru disisipkan di baris", line_num)

# === SISIPKAN ARTIKEL BARU SETELAH PAGINATION ===
pagination_pattern = re.search(r'(<div class="pagination".*?</div>)', h, re.DOTALL)
if pagination_pattern:
    insert_pos = pagination_pattern.end()
    # Urutan: a127 (terbaru) paling atas, lalu a126, lalu a125
    artikel_block = '\n' + a127 + '\n' + a126 + '\n' + a125 + '\n'
    h = h[:insert_pos] + artikel_block + h[insert_pos:]
    print("Artikel baru disisipkan setelah pagination")
else:
    print("ERROR: pagination tidak ditemukan")

# === SCAN KARAKTER CJK/CYRILLIC ===
bad = re.findall(r'[\u4e00-\u9fff\u0400-\u04ff]', h)
if bad:
    print("KARAKTER CJK/CYRILLIT DITEMUKAN:", bad[:10])
else:
    print("Scan CJK/Cyrillic: BERSIH")

# Simpan
P.write_text(h, encoding='utf-8')
print("File disimpan. Ukuran:", len(h), "bytes")
