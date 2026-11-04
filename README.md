# Topologi: Pendekatan Berbasis Inkuiri — terjemahan Bahasa Indonesia *Topology: An Inquiry-Based Approach*

Terjemahan Bahasa Indonesia yang lengkap dari buku teks terbuka *Topology: An Inquiry-Based Approach* karya Steven
Schlicker (Grand Valley State University), seluruh 20 bab, beserta pendamping belajar mandiri, delapan modul pelengkap,
dan laboratorium epsilon-delta yang ditulis baru, sebagai pembaca HTML, PDF 645 halaman, sumber PreTeXt, dan backend
modular.

[Baca daring](https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/) · [Unduh PDF](https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/downloads/topologi-pendekatan-berbasis-inkuiri-edisi-lengkap-id.pdf)

## Cara pembuatan

Terjemahan, materi pendamping, backend modular, dan pemeriksaan dikerjakan oleh AI: OpenAI Codex gpt-5.6-sol, Ultra.
Terjemahan mempertahankan struktur PreTeXt, pengenal, rumus, kegiatan, latihan, dan hubungan silang; koreksi sumber yang
bersifat deterministik dicatat terpisah. Pemeriksaan mencakup struktur sumber, validasi RelaxNG, audit matematika
pendamping, pembangunan HTML deterministik, dua pembangunan PDF yang identik byte demi byte, tautan, aset, dan runtime
luring, reflow desktop dan seluler, serta inspeksi visual seluruh 645 halaman. Pada 1 September 2026 istilah
dibandingkan dengan bahan ajar topologi berbahasa Indonesia dari UNDIP Press dan Universitas Terbuka; empat pemakaian
*ruang topologis* diseragamkan menjadi *ruang topologi*
(`qa/NATIVE_INDONESIAN_TERMINOLOGY_QA_2026-08-31.md`).

## Status

Edisi lengkap: seluruh 20 bab, pendamping untuk setiap bab, dan delapan modul pelengkap. PDF belum bertag, dan sebagian
font matematika PDF belum memiliki pemetaan Unicode lengkap; HTML adalah permukaan aksesibilitas utama. Masih mungkin
ada kesalahan.

## Isi

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

Tambahan orisinal:

- pendamping belajar mandiri untuk seluruh 20 bab, dengan petunjuk, jawaban, rubrik, dan solusi bertahap;
- delapan modul pelengkap tentang separasi, keterhitungan, jaring, hasil kali sebarang, kekompakan lokal, metrisasi,
  ruang fungsi, dan penguasaan terpadu, semuanya dengan solusi lengkap;
- laboratorium epsilon-delta luring sebagai pengganti aplet Bab 6 yang tidak terarsipkan;
- backend modular netral-lokal untuk provenans, istilah, latihan, solusi, koreksi sumber, hak komponen, dan status
  pemeriksaan.

Struktur repositori: `source/` (sumber PreTeXt dan pembungkus pembaca), `companion/` (pendamping), `backend/`
(pemetaan JSON/CSV; manifes edisi `backend/complete_edition_source_backend_manifest.json`), `assets/`, `publication/`,
`xsl/` (aset dan konfigurasi), `qa/` (manifes, hash, dan hasil pemeriksaan), `docs/` (situs GitHub Pages).

Membangun (Python 3.12.13, PreTeXt 1.7.5, setuptools 75.8.0, MiKTeX 26.5; runtime MathJax, Lunr, dan PreTeXt
dibundel secara lokal):

```text
pretext build chapters01-20-complete-html --clean
python scripts/finalize_and_qa_chapter20_complete_html.py
python scripts/finalize_and_qa_chapter20_complete_html.py --check
python scripts/qa_chapters01_20_complete_pdf_pipeline.py config
pwsh -File scripts/run_complete_pdf_pipeline_with_mutex.ps1
```

## Sumber dan atribusi

- Steven Schlicker, *Topology: An Inquiry-Based Approach*, Grand Valley State University
  ([rekaman institusional](https://scholarworks.gvsu.edu/books/30/), [repositori](https://github.com/gvsuoer/topology),
  commit `0c2d8f614ef87aa00de373f3418146c2f1d13bb9`).
- Versi web dimungkinkan oleh PreTeXt dan pekerjaan Rob Beezer serta komunitas PreTeXt. David Farmer di American
  Institute of Mathematics menyediakan konversi awal; Ian Curtis, Editorial Assistant GVSU Libraries, mengembangkan versi
  PreTeXt dengan dukungan University Libraries dan GVSU President's Innovation Fund.
- Edisi ini tidak didukung atau disahkan oleh Steven Schlicker, GVSU, PreTeXt, atau repositori sumber.

## Lisensi

Terjemahan buku diperlakukan secara konservatif sebagai CC BY-NC-SA 3.0 karena metadata resmi dan prakata tidak
konsisten. Pendamping dan laboratorium epsilon-delta adalah komponen terpisah berlisensi CC BY 4.0. Perangkat lunak,
XSLT, font, dan gambar dengan pemberitahuan sendiri mempertahankan hak masing-masing. Lihat [LICENSES.md](LICENSES.md)
dan [companion/RIGHTS.md](companion/RIGHTS.md).
