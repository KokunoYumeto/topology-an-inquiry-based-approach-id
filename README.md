# *Topologi: Pendekatan Berbasis Inkuiri* - Bahasa Indonesia

Edisi Bahasa Indonesia yang sedang diproduksi dari *Topology: An Inquiry-Based
Approach* karya Steven Schlicker, Grand Valley State University.

**Baca edisi web:**  
https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/

**Unduh PDF batas terverifikasi Bab 1-6 (133 halaman):**

https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-06-id.pdf

## Status

Produksi lengkap masih berlangsung. Batas publik saat ini memuat:

- Bab 1, *Himpunan*;
- Bab 2, *Fungsi*;
- Bab 3, *Ruang Metrik*;
- Bab 4, *Penerapan Ruang Metrik*;
- Bab 5, *Batas Bawah Terbesar*;
- Bab 6, *Fungsi Kontinu di Ruang Metrik*;
- pendamping belajar mandiri orisinal untuk keenam bab, dengan petunjuk,
  jawaban, rubrik, dan solusi bertahap;
- laboratorium epsilon-delta orisinal yang dapat digunakan secara luring untuk
  menggantikan kebergantungan aplet Bab 6 yang tidak terarsipkan; dan
- backend modular netral-lokal untuk provenance, istilah, latihan, solusi,
  koreksi sumber, hak komponen, dan status QA.

Batas Bab 1-6 telah melewati pemeriksaan struktur sumber, validasi RelaxNG,
audit matematika
pendamping, dua pembangunan HTML deterministik, dua pembangunan PDF ketat,
pemeriksaan tautan/aset, reflow desktop/seluler, interaksi petunjuk, dan
inspeksi visual seluruh 133 halaman. Kolom baca desktop menggunakan lebar 960
px dan terpusat di panel utama; versi seluler mengalir ulang tanpa luapan
horizontal. Ini bukan klaim bahwa edisi 20 bab sudah
selesai.

## Sumber resmi yang dibekukan

- Rekor institusional:
  https://scholarworks.gvsu.edu/books/30/
- Repositori resmi:
  https://github.com/gvsuoer/topology
- Commit:
  `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`
- Tree:
  `7df245934eedb7174d5ff8af18afff5a7abdde78`
- SHA-256 arsip resmi:
  `d7cadeb10e6525568a90340bceadbc77dc1e5620053e257e8b3126acb8ce01f3`

Terjemahan mempertahankan struktur PreTeXt, pengenal, rumus, kegiatan,
latihan, dan hubungan silang. Koreksi sumber yang bersifat deterministik
dicatat terpisah; tidak ada dukungan resmi dari Steven Schlicker, GVSU,
PreTeXt, atau repositori sumber yang dinyatakan maupun disiratkan.

## Struktur repositori

- `source/` - sumber PreTeXt dan pembungkus pembaca;
- `companion/` - pendamping belajar mandiri orisinal;
- `backend/` - pemetaan modular JSON/CSV;
- `assets/`, `publication/`, dan `xsl/` - aset dan konfigurasi bangun;
- `qa/` - manifest, hash, dan kuitansi pemeriksaan;
- `docs/` - byte pembaca publik untuk GitHub Pages.

Manifest kumulatif yang mengikat batas ini adalah
`qa/CHAPTER06_SOURCE_MANIFEST.json`; kuitansi manusia-bacanya adalah
`qa/CHAPTER06_BUILD_QA.md`.

## Membangun batas saat ini

Lingkungan yang direkam memakai Python 3.12.13, PreTeXt 1.7.5,
setuptools 75.8.0, dan MiKTeX 26.5.

```text
pretext build chapters01-06-html --clean
python scripts/finalize_chapter01_html.py output/chapters01-06-html --manifest qa/CHAPTER06_HTML_MANIFEST.json
python scripts/build_pretext_pdf_strict.py chapters01-06-pdf --clean --mainmatter-physical-page 7 --log qa/CHAPTER06_PDF_BUILD_RUN2.log --expect-pdf output/chapters01-06-pdf/chapters_01_06_reader.pdf
```

HTML saat ini masih memanggil beberapa dependensi runtime jarak jauh dari
PreTeXt, Runestone, MathJax, dan penyedia font. Penutupan luring penuh tetap
merupakan gerbang rilis edisi lengkap. PDF belum bertag; HTML adalah permukaan
aksesibilitas utama.

## Hak dan atribusi

Terjemahan spine GVSU diperlakukan secara konservatif sebagai
CC BY-NC-SA 3.0 karena metadata resmi dan prosa prakata tidak konsisten.
Pendamping dan laboratorium epsilon-delta yang ditulis baru merupakan komponen
terpisah berlisensi CC BY 4.0.
Perangkat lunak, XSLT, font, dan gambar yang diberi pemberitahuan tersendiri
mempertahankan hak masing-masing. Lihat `LICENSES.md` dan
`companion/RIGHTS.md`; tidak ada lisensi payung yang meratakan seluruh
koleksi.

## Asal konversi PreTeXt

Versi web dimungkinkan oleh PreTeXt dan pekerjaan Rob Beezer serta komunitas
PreTeXt. David Farmer di American Institute of Mathematics menyediakan
konversi awal; Ian Curtis, Editorial Assistant GVSU Libraries, kemudian
mengembangkan versi PreTeXt dengan dukungan University Libraries dan GVSU
President's Innovation Fund.
