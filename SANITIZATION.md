# Standar Sanitasi

Repositori publik dapat di-fork, di-cache, diindeks mesin pencari, dan disalin
sebelum sebuah commit dihapus. Sanitasi harus dilakukan **sebelum** query masuk
working tree Git, dikirim ke AI, dibagikan dalam issue, atau dimasukkan ke pull
request.

## Data yang Wajib Dihapus

Ganti atau hapus seluruh nilai yang dapat mengidentifikasi lingkungan, antara
lain:

- nama organisasi, customer, unit bisnis, proyek, atau vendor lokal;
- singkatan organisasi dan kode lokasi yang hanya dipahami internal;
- ID, nama, hostname, atau IP kolektor;
- hostname, domain, FQDN, IP, subnet, MAC address, dan topologi jaringan;
- username, nama orang, email, nomor telepon, dan identifier akun;
- UUID, tenant ID, asset ID, rule ID, case ID, incident ID, dan ticket ID;
- password, token, API key, cookie, hash kredensial, dan connection string;
- nama file, direktori, bucket, share, database, atau tabel internal;
- event mentah, hasil query, log, screenshot, export, dan packet capture;
- rentang waktu insiden atau operasi yang dapat dikorelasikan;
- zona waktu, ambang SLA, maintenance window, dan nilai kebijakan khusus; serta
- komentar SQL, nama berkas, judul, metadata, dan riwayat commit yang memuat
  konteks sensitif.

Pseudonim seperti `CLIENT-A` tidak selalu aman. Kombinasi industri, lokasi,
hostname, tanggal, dan pola event dapat mengidentifikasi pihak yang dimaksud.
Gunakan placeholder generik tanpa mempertahankan hubungan dengan nama asli.

## Placeholder Standar

Gunakan format `{{UPPER_SNAKE_CASE}}`.

| Kategori | Placeholder |
| --- | --- |
| Organisasi/customer | `{{CUSTOMER_NAME}}` |
| ID kolektor | `{{COLLECTOR_ID}}` |
| Nama kolektor | `{{COLLECTOR_NAME}}` |
| Batas waktu | `{{PERIOD_START}}`, `{{PERIOD_END}}` |
| Zona waktu | `{{TIMEZONE}}` |
| IP atau subnet | `{{SOURCE_IP}}`, `{{TARGET_NETWORK}}` |
| Host atau domain | `{{HOST_NAME}}`, `{{DOMAIN_NAME}}` |
| Nilai kebijakan | `{{TARGET_PERCENT}}` |

Placeholder string tetap berada di dalam tanda petik SQL. Placeholder numerik
tidak diberi tanda petik kecuali fungsi konversi query memang mengharuskannya.

## Data Dummy Standar

Template kanonik tetap menggunakan placeholder. Berkas
`query.example.sql.tmpl` mengganti placeholder dengan nilai dummy standar:

| Parameter | Nilai dummy |
| --- | --- |
| `CUSTOMER_NAME` | `Dummy_Organisasi` |
| `COLLECTOR_NAME` | `Dummy_Kolektor` |
| `COLLECTOR_ID` | `999999` |
| `PERIOD_START` | `2026-08-17 00:00:00` |
| `PERIOD_END` | `2026-08-18 00:00:00` |
| `TIMEZONE` | `UTC` |
| `HEARTBEAT_WINDOW_SECONDS` | `600` |
| `TARGET_PERCENT` | `90` |
| `DELAY_THRESHOLD_SECONDS` | `3600` |

Nilai dummy tidak boleh berasal dari transformasi nama atau ID sebenarnya.
`COLLECTOR_ID` bertipe numerik, sehingga gunakan `999999`, bukan string
`ID_Dummy_Kolektor`. Format tanggal ClickHouse adalah
`YYYY-MM-DD HH:MM:SS`, bukan `DD-MM-YYYY HH:MM:SS`.

Panduan penggunaan lengkap tersedia di
[DUMMY_DATA_GUIDE.md](DUMMY_DATA_GUIDE.md).

## Alur Publikasi

1. Simpan query asli hanya di lokasi privat yang berwenang.
2. Buat salinan kerja di luar repositori publik.
3. Inventarisasi identitas, infrastruktur, waktu, kebijakan, dan data hasil.
4. Ganti nilai dengan placeholder standar.
5. Hapus komentar, judul, dan nama berkas yang masih mengandung konteks asli.
6. Tinjau query sebagai penyerang yang mencoba menebak sumbernya.
7. Masukkan hanya template tersanitasi dan contoh dummy ke folder `queries/`.
8. Pastikan contoh dummy tidak memuat placeholder atau nilai sebenarnya.
9. Jalankan validator lokal.
10. Periksa diff dan riwayat Git sebelum push.
11. Minta review manusia lain untuk query berisiko tinggi.

Daftar nama customer sebenarnya tidak boleh disimpan sebagai denylist di
repositori publik. Pemeriksaan nama internal tambahan dapat dijalankan secara
lokal dengan daftar yang tidak dilacak Git.

## Batas AI

AI hanya boleh menerima versi yang sudah melewati sanitasi manusia. Jangan
mengandalkan AI untuk menemukan seluruh data sensitif. AI dapat membantu memberi
judul dan menyusun penjelasan, tetapi hasilnya harus diperiksa terhadap SQL dan
dokumentasi resmi.

Jangan memasukkan hasil query produksi ke AI, bahkan ketika nama kolom terlihat
generik. Nilai, distribusi, timestamp, dan kombinasi atribut dapat tetap menjadi
informasi rahasia.

## Pemeriksaan Otomatis

```bash
python3 scripts/validate_catalog.py
```

Validator menolak beberapa pola umum dan artefak mentah, tetapi tidak memahami
seluruh kosakata internal organisasi. Lolos validator bukan jaminan anonimitas,
kepemilikan, keamanan, atau kepatuhan hukum.

## Checklist Review Manusia

- [ ] Judul dan nama folder tidak memuat organisasi atau kode lokasi.
- [ ] Tidak ada nama customer, ID, hostname, IP, domain, atau username nyata.
- [ ] Tidak ada tanggal, zona waktu, atau target kebijakan khusus yang tertanam.
- [ ] Tidak ada secret, hasil query, event mentah, screenshot, atau export.
- [ ] Semua nilai deployment menjadi placeholder yang dideklarasikan.
- [ ] Penjelasan tidak mengungkap konteks yang telah dihapus dari SQL.
- [ ] Metadata mencatat status sanitasi dan sumber judul dengan benar.
- [ ] Rujukan pihak ketiga berupa tautan dan ringkasan orisinal.
- [ ] Kontributor berhak mempublikasikan dan melisensikan materi tersebut.
- [ ] Diff serta commit sebelumnya tidak mengandung versi belum tersanitasi.

## Jika Terjadi Kebocoran

Jangan membuka issue publik. Ikuti [SECURITY.md](SECURITY.md), hentikan distribusi,
rotasi secret bila ada, dan nilai kebutuhan penghapusan dari seluruh riwayat
Git. Menghapus berkas pada commit baru tidak menghapusnya dari commit lama,
fork, cache, atau clone yang sudah ada.