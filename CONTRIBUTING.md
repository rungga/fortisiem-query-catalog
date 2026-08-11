# Berkontribusi

Kontribusi diterima untuk kepentingan belajar dan penggunaan bersama selama
materinya orisinal, tersanitasi, terdokumentasi, dan dapat dilisensikan secara
sah oleh kontributor.

## Pernyataan Kontributor

Dengan mengirim kontribusi, Anda menyatakan bahwa:

- kontribusi tersebut adalah karya asli Anda atau Anda memiliki hak tertulis
  untuk mempublikasikan dan melisensikannya;
- kontribusi tidak melanggar kewajiban kerja, kontrak customer, NDA, lisensi
  produk, hak cipta, merek, privasi, atau kebijakan yang berlaku;
- tidak ada data rahasia, data pribadi, kredensial, hasil produksi, atau materi
  pihak ketiga yang tidak diizinkan; dan
- kontribusi dilisensikan di bawah MIT License repositori ini.

Jangan mengirim query hanya karena nama organisasi telah diganti. Hak publikasi
dan seluruh konteks sensitif tetap harus diperiksa.

## Menambahkan Query

1. Baca [SANITIZATION.md](SANITIZATION.md) dan sanitasi di luar working tree.
2. Buat folder `queries/<category>/<ID>-<slug>/`.
3. Tambahkan `query.sql.tmpl`, `query.example.sql.tmpl`, `metadata.json`, dan
  `README.md`.
4. Gunakan placeholder `{{UPPER_SNAKE_CASE}}` untuk seluruh nilai deployment.
5. Isi contoh siap copy-paste hanya dengan data dummy standar dari
  [DUMMY_DATA_GUIDE.md](DUMMY_DATA_GUIDE.md).
6. Jelaskan tujuan, setiap blok logika, formula, kolom hasil, asumsi,
   keterbatasan, performa, dan skenario validasi.
7. Tautkan dokumentasi resmi yang relevan dan catat versi serta tanggal akses.
8. Perbarui [INDEX.md](INDEX.md).
9. Jalankan validator dan tinjau seluruh diff sebelum membuka pull request.

Maintainer dapat menyesuaikan ID agar tetap unik.

## Judul dengan Bantuan AI

AI boleh mengusulkan judul hanya setelah query disanitasi. Judul harus
menjelaskan apa yang benar-benar dihitung, bukan membuat klaim yang lebih kuat
daripada data. Catat `ai-assisted` pada `title.source` dan tetapkan
`reviewed_by_maintainer` setelah review manusia.

Contoh: query yang hanya menilai kontinuitas heartbeat sebaiknya menggunakan
istilah "observed uptime" atau "heartbeat availability", bukan menyatakan uptime
perangkat secara absolut.

## Dokumentasi Pihak Ketiga

- Tautkan halaman resmi yang relevan.
- Tulis ringkasan dan penjelasan dengan kata-kata sendiri.
- Jangan menyalin paragraf, tabel, screenshot, diagram, logo, atau contoh query
  dari dokumentasi Fortinet.
- Jangan menyatakan proyek ini resmi, tersertifikasi, atau didukung Fortinet.
- Tandai klaim yang belum diuji dan jangan mengarang kompatibilitas versi.

## Validasi

```bash
python3 scripts/validate_catalog.py
```

Pull request harus membuat workflow `Validate catalog` lulus. Validator tidak
menggantikan review teknis, privasi, dan kepemilikan.

## Yang Tidak Boleh Dikirim

- query yang telah berisi nilai deployment nyata;
- contoh query yang masih memiliki placeholder atau data yang menyerupai
  deployment nyata;
- hasil pencarian, raw event, log, export, screenshot, atau packet capture;
- secret dalam bentuk aktif maupun yang dianggap sudah kedaluwarsa;
- materi internal organisasi atau customer;
- salinan dokumentasi atau contoh milik pihak lain; dan
- SQL mutatif atau administratif.

Untuk melaporkan data sensitif yang telanjur masuk, gunakan proses privat dalam
[SECURITY.md](SECURITY.md), bukan issue atau komentar pull request.