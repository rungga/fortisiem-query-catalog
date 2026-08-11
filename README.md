# FortiSIEM Community Query Catalog

Katalog open-source berisi query FortiSIEM yang tersanitasi dan dijelaskan
langkah demi langkah. Tujuannya bukan hanya menyediakan query siap adaptasi,
tetapi membantu pembaca memahami logika, asumsi, hasil, dan keterbatasannya.

Query awal dalam repositori ini adalah karya asli **Rungga**. Judul dapat dibuat
dengan bantuan AI setelah query disanitasi, kemudian ditinjau oleh maintainer.

> [!IMPORTANT]
> Proyek ini independen dan tidak berafiliasi, disponsori, atau didukung oleh
> Fortinet. Jangan mengirim query, hasil pencarian, atau data lingkungan yang
> belum disanitasi ke layanan AI atau repositori publik.

Lihat [Panduan Data Dummy dan Copy-Paste FortiSIEM](DUMMY_DATA_GUIDE.md) untuk
contoh nilai aman dan langkah menjalankan seluruh query melalui Query Console.

## Katalog

Lihat [INDEX.md](INDEX.md) untuk seluruh query.

| ID | Query | Fokus |
| --- | --- | --- |
| [FSQ-AVAIL-001](queries/availability/FSQ-AVAIL-001-observed-single-collector-uptime/) | Uptime Teramati Satu Kolektor dari Heartbeat Sistem | Availability satu kolektor |
| [FSQ-DQ-001](queries/data-quality/FSQ-DQ-001-parsed-event-source-timestamp-coverage-and-ingestion-delay-anomalies/) | Cakupan Timestamp Sumber dan Anomali Delay Ingesti pada Event Terurai | Coverage timestamp dan anomali delay ingestion |

## Isi Setiap Query

Setiap folder query wajib memiliki:

- `query.sql.tmpl`: SQL tersanitasi dengan placeholder eksplisit;
- `query.example.sql.tmpl`: SQL lengkap dengan data dummy yang siap
    di-copy-paste ke FortiSIEM;
- `metadata.json`: judul, kategori, parameter, status privasi, kompatibilitas,
  dan rujukan terstruktur; serta
- `README.md`: tujuan, pembahasan setiap blok, formula, hasil, asumsi,
  keterbatasan, performa, validasi, dan rujukan resmi.

Status "tersanitasi" tidak berarti query otomatis aman untuk dipublikasikan.
Pemindaian otomatis hanya menemukan pola umum; review manusia tetap wajib.

## Cara Menggunakan

1. Baca dokumentasi query sampai bagian asumsi dan keterbatasan.
2. Buka `query.example.sql.tmpl` untuk melihat query lengkap dengan data dummy.
3. Salin seluruh query ke **Analytics > Advanced Search > Query Console**.
4. Untuk penggunaan nyata, ganti dummy hanya pada salinan lokal di luar Git.
5. Pastikan tipe, quoting, rentang waktu, dan filter sudah benar.
6. Klik **Format**, periksa error, lalu jalankan pada periode data yang kecil.
7. Bandingkan hasil dengan sumber data yang telah diketahui.
8. Jangan commit salinan berisi data nyata atau hasil query.

FortiSIEM Advanced Search menggunakan SQL untuk menelusuri Event Database
ClickHouse. Berdasarkan dokumentasi Fortinet 7.5.1, Advanced Search hanya
menyediakan statement `SELECT`. Periksa dokumentasi untuk versi deployment Anda
sebelum menggunakan query dari katalog ini.

## Struktur Repositori

```text
.
├── queries/               # Query tersanitasi dan dokumentasinya
├── schema/                # Kontrak metadata JSON
├── scripts/               # Validator lokal dan CI
├── .github/workflows/     # Pemeriksaan otomatis
├── INDEX.md               # Indeks query
├── DUMMY_DATA_GUIDE.md    # Data dummy dan alur copy-paste FortiSIEM
├── SANITIZATION.md        # Standar penghapusan data sensitif
├── CONTRIBUTING.md        # Aturan kontribusi
├── SECURITY.md            # Pelaporan kebocoran secara privat
├── NOTICE.md              # Kepemilikan dan pemberitahuan merek
└── LICENSE                # MIT License
```

## Validasi

Memerlukan Python 3.10 atau lebih baru dan tidak memakai dependensi eksternal.

```bash
python3 scripts/validate_catalog.py
```

Validator memeriksa struktur, metadata, kecocokan placeholder, dokumentasi
wajib, statement SQL, artefak mentah, serta pola umum seperti IP, email, UUID,
tanggal operasional, customer literal, dan identitas kolektor literal.

## Penggunaan AI

AI boleh membantu:

- mengusulkan judul yang deskriptif;
- menyusun ringkasan dan pembahasan awal; dan
- menemukan bagian yang perlu dijelaskan atau diuji.

AI tidak boleh menerima data mentah yang mengandung identitas organisasi,
topologi, kredensial, hasil query, atau informasi kontraktual. Seluruh materi
hasil bantuan AI harus ditinjau maintainer; AI bukan sumber kebenaran teknis.

## Rujukan Resmi

- [FortiSIEM Documentation Library](https://docs.fortinet.com/product/fortisiem)
- [FortiSIEM Advanced Search Overview](https://docs.fortinet.com/document/fortisiem/7.5.1/user-guide/704751/overview)
- [Creating a New Advanced Search](https://docs.fortinet.com/document/fortisiem/7.5.1/user-guide/431900/creating-a-new-advanced-search)
- [Fortinet Legal Terms](https://www.fortinet.com/corporate/about-us/legal)

Repositori hanya menautkan rujukan resmi dan menulis penjelasan orisinal. Materi
dokumentasi, gambar, tabel, logo, dan contoh milik Fortinet tidak disalin atau
dilisensikan ulang di sini.

## Lisensi

Karya asli dalam repositori ini tersedia dengan [MIT License](LICENSE). Lihat
[NOTICE.md](NOTICE.md) untuk batas cakupan lisensi, atribusi, penggunaan merek,
dan penafian hubungan dengan Fortinet.

Setiap pengguna bertanggung jawab memvalidasi query dan mematuhi hukum,
kontrak, lisensi produk, serta kebijakan organisasinya sendiri.