# *Topologi: Pendekatan Berbasis Inkuiri* - Bahasa Indonesia

Edisi Bahasa Indonesia lengkap dari *Topology: An Inquiry-Based Approach*
karya Steven Schlicker, Grand Valley State University, beserta pendamping
belajar mandiri dan pelengkap C90 yang ditulis terpisah.

**Baca edisi lengkap:**

https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/

**Unduh PDF edisi lengkap (645 halaman):**

https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/downloads/topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf

**Arsip Zenodo dalam satu riwayat versi:**

https://doi.org/10.5281/zenodo.22059894

## Status

Pemutakhiran terminologi 1 September 2026 membandingkan istilah edisi ini
dengan sumber pengajaran topologi berbahasa Indonesia dari UNDIP Press dan
Universitas Terbuka. Empat pemakaian *ruang topologis* diseragamkan menjadi
*ruang topologi*; keputusan, batas bukti, dan istilah yang sengaja dipertahankan
dicatat di `qa/NATIVE_INDONESIAN_TERMINOLOGY_QA_2026-08-31.md`.

Edisi terverifikasi memuat seluruh 20 bab:

- Bab 1, *Himpunan*;
- Bab 2, *Fungsi*;
- Bab 3, *Ruang Metrik*;
- Bab 4, *Penerapan Ruang Metrik*;
- Bab 5, *Batas Bawah Terbesar*;
- Bab 6, *Fungsi Kontinu di Ruang Metrik*;
- Bab 7, *Bola Terbuka dan Lingkungan pada Ruang Metrik*;
- Bab 8, *Himpunan Terbuka dalam Ruang Metrik*;
- Bab 9, *Barisan di Ruang Metrik*;
- Bab 10, *Himpunan Tertutup dalam Ruang Metrik*;
- Bab 11, *Subruang dan Hasil Kali Ruang Metrik*;
- Bab 12, *Ruang Topologi*;
- Bab 13, *Himpunan Tertutup dalam Ruang Topologi*;
- Bab 14, *Kekontinuan dan Homeomorfisme*;
- Bab 15, *Subruang*;
- Bab 16, *Ruang Hasil Bagi*;
- Bab 17, *Ruang Kompak*;
- Bab 18, *Ruang Topologi Terhubung*;
- Bab 19, *Ruang Terhubung Lintasan*;
- Bab 20, *Hasil Kali Ruang Topologi*;
- pendamping belajar mandiri orisinal untuk seluruh 20 bab, dengan petunjuk,
  jawaban, rubrik, dan solusi bertahap;
- delapan modul pelengkap C90 orisinal tentang separasi, keterhitungan, jaring,
  hasil kali sebarang, kekompakan lokal, metrisasi, ruang fungsi, dan penguasaan
  terpadu, semuanya dengan solusi lengkap;
- laboratorium epsilon-delta orisinal yang dapat digunakan secara luring untuk
  menggantikan kebergantungan aplet Bab 6 yang tidak terarsipkan; dan
- backend modular netral-lokal untuk provenance, istilah, latihan, solusi,
  koreksi sumber, hak komponen, dan status QA.

Edisi lengkap telah melewati pemeriksaan struktur sumber, validasi RelaxNG,
audit matematika pendamping, pembangunan HTML deterministik, dua pembangunan
PDF ketat yang identik byte demi byte, pemeriksaan tautan/aset dan penutupan
runtime luring, reflow desktop/seluler, interaksi petunjuk, serta inspeksi
visual seluruh 645 halaman. HTML final memuat 22.613 berkas / 89.005.555 byte
dengan SHA-256 manifest kanonis
`cefa760a525bd797a235a1cec2277fd9bc5fe4bf81e0cd12dc03c2f6fd668cb7`.
Kolom baca menggunakan ukuran 960 px pada desktop lebar dan 600 px pada
desktop ringkas/tablet, selalu terpusat di panel utama; versi seluler mengalir
ulang tanpa luapan horizontal.

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

Catatan provenance alat: draf terjemahan, materi pendamping, backend modular,
dan pemeriksaan edisi ini diproduksi oleh **OpenAI Codex gpt-5.6-sol, Ultra**,
atas arahan pengguna. Catatan ini tidak menggantikan kredit penulis, sumber,
institusi, atau kontributor manusia yang dipertahankan di seluruh edisi.

## Struktur repositori

- `source/` - sumber PreTeXt dan pembungkus pembaca;
- `companion/` - pendamping belajar mandiri orisinal;
- `backend/` - pemetaan modular JSON/CSV;
- `assets/`, `publication/`, dan `xsl/` - aset dan konfigurasi bangun;
- `qa/` - manifest, hash, dan kuitansi pemeriksaan;
- `docs/` - byte pembaca publik untuk GitHub Pages.

Manifest sumber/backend yang mengikat edisi lengkap adalah
`backend/complete_edition_source_backend_manifest.json`; bukti pembaca final
ada di `qa/CHAPTER20_COMPLETE_HTML_QA.json`,
`qa/CHAPTERS01_20_COMPLETE_PDF_QA.json`, dan
`qa/CHAPTER20_COMPLETE_DOCS_QA.json`.

## Membangun edisi lengkap

Lingkungan yang direkam memakai Python 3.12.13, PreTeXt 1.7.5,
setuptools 75.8.0, dan MiKTeX 26.5.

```text
pretext build chapters01-20-complete-html --clean
python scripts/finalize_and_qa_chapter20_complete_html.py
python scripts/finalize_and_qa_chapter20_complete_html.py --check
python scripts/qa_chapters01_20_complete_pdf_pipeline.py config
pwsh -File scripts/run_complete_pdf_pipeline_with_mutex.ps1
```

Runtime MathJax, Lunr, dan PreTeXt yang diperlukan pembaca telah dipatok dan
dibundel secara lokal; pemeriksaan penutupan luring dan privasi lulus tanpa
referensi runtime jarak jauh. PDF belum bertag, sehingga HTML tetap menjadi
permukaan aksesibilitas utama. Sebagian font matematika PDF juga belum memiliki
pemetaan Unicode yang lengkap, sehingga ekstraksi teks matematika dari PDF
tidak selalu andal meskipun tampilan visualnya lolos pemeriksaan.

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
