# Panduan Data Dummy dan Copy-Paste FortiSIEM

Setiap query dalam katalog menyediakan dua berkas:

- `query.sql.tmpl` adalah template kanonik dengan placeholder seperti
  `{{CUSTOMER_NAME}}`. Berkas ini aman untuk publikasi, tetapi belum dapat
  dijalankan sebelum placeholder diganti.
- `query.example.sql.tmpl` adalah query lengkap dengan data dummy. Seluruh
  isinya dapat langsung disalin ke FortiSIEM untuk melihat bentuk query yang
  valid. Nilai dummy biasanya tidak cocok dengan data deployment sehingga hasil
  kosong adalah hal yang wajar.

Data dummy bukan data yang harus dibuat di FortiSIEM. Nilai tersebut hanya
contoh aman untuk menunjukkan posisi, format, tipe, dan quoting parameter.

## Data Dummy Standar

| Kebutuhan | Nilai dummy | Catatan |
| --- | --- | --- |
| Nama organisasi/customer | `Dummy_Organisasi` | String, gunakan tanda petik tunggal dalam SQL |
| Nama kolektor | `Dummy_Kolektor` | String, gunakan tanda petik tunggal |
| ID kolektor | `999999` | Numerik, jangan gunakan tanda petik |
| Period start | `2026-08-17 00:00:00` | Format ClickHouse `YYYY-MM-DD HH:MM:SS` |
| Period end | `2026-08-18 00:00:00` | Harus lebih besar dari period start |
| Timezone | `UTC` | Zona waktu IANA yang netral |
| Heartbeat window | `600` | Contoh numerik dalam detik |
| Target persentase | `90` | Contoh numerik 0 sampai 100 |
| Delay threshold | `3600` | Contoh numerik dalam detik |

`ID_Dummy_Kolektor` tidak boleh dimasukkan ke `COLLECTOR_ID` karena kolom
tersebut numerik. Gunakan `999999` sebagai ID dummy dan `Dummy_Kolektor` sebagai
nama dummy.

Penulisan `17-08-2026 00:00:00` juga tidak digunakan di query. Untuk
`toDateTime`, tulis tahun lebih dahulu: `2026-08-17 00:00:00`.

## Cara Copy-Paste ke FortiSIEM

1. Buka folder query yang ingin digunakan.
2. Buka `query.example.sql.tmpl`.
3. Salin seluruh isi berkas, termasuk bagian `WITH` sampai `LIMIT`.
4. Untuk sekadar mempelajari sintaks, biarkan nilai dummy apa adanya.
5. Untuk menjalankan pada deployment yang berwenang, buat salinan lokal di luar
   working tree Git dan ganti hanya nilai dummy dengan nilai yang sah.
6. Di FortiSIEM, buka **Analytics > Advanced Search > Query Console**.
7. Jika query memakai atribut yang tidak tampil pada Database Schema, pilih
   atribut tersebut melalui **Attributes used**.
8. Tempel seluruh query, klik **Format**, periksa error, lalu klik **Run**.
9. Mulai dengan periode pendek dan bandingkan hasil dengan data yang telah
   diketahui.

FortiSIEM menerima seluruh SQL Advanced Search melalui copy-paste pada Query
Console. Jangan menyalin hanya potongan CTE karena query harus ditempel sebagai
satu kesatuan.

## Contoh yang Tersedia

- [Contoh dummy uptime satu kolektor](queries/availability/FSQ-AVAIL-001-observed-single-collector-uptime/query.example.sql.tmpl)
- [Contoh dummy kualitas timestamp dan delay ingestion](queries/data-quality/FSQ-DQ-001-parsed-event-source-timestamp-coverage-and-ingestion-delay-anomalies/query.example.sql.tmpl)
- [Contoh dummy pencarian indikator potensi SQL injection](queries/threat-hunting/FSQ-HUNT-001-potential-sql-injection-indicator-matches/query.example.sql.tmpl)
- [Contoh dummy pencarian referensi file shadow Linux](queries/threat-hunting/FSQ-HUNT-002-potential-linux-shadow-file-reference-matches/query.example.sql.tmpl)

## Aturan Keamanan

- Jangan commit query yang telah berisi nilai deployment nyata.
- Jangan commit hasil query, raw event, screenshot, hostname, IP, atau export.
- Jangan mengirim nilai produksi ke layanan AI.
- Jangan menganggap hasil kosong dari data dummy sebagai kegagalan query.
- Tinjau kembali tipe parameter: string memakai tanda petik, numerik tidak.
- Jalankan hanya query `SELECT` yang telah ditinjau dan diizinkan.

Setelah pengujian selesai, hapus salinan lokal yang berisi data nyata bila tidak
lagi dibutuhkan sesuai kebijakan organisasi.