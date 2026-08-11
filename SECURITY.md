# Security Policy

## Cakupan

Kebocoran data sensitif, credential, identitas customer, detail infrastruktur,
atau materi yang tidak berhak dipublikasikan dianggap sebagai masalah keamanan
repositori.

Masalah operasional pada produk Fortinet bukan berada di bawah pengelolaan
proyek ini dan harus dilaporkan melalui kanal resmi Fortinet yang sesuai.

## Pelaporan Privat

Jangan membuat issue, discussion, pull request, atau komentar publik yang
mengulang data sensitif.

Gunakan fitur **Security > Report a vulnerability** pada repositori GitHub bila
tersedia. Jika fitur tersebut belum aktif, hubungi maintainer melalui kanal
privat pada profil GitHub-nya dan cukup sebutkan bahwa ada potensi kebocoran.

Sertakan hanya informasi minimum:

- path berkas dan commit yang terdampak;
- kategori data yang terekspos;
- apakah nilai tersebut masih aktif; dan
- tindakan mendesak yang disarankan.

Jangan menyalin secret atau nilai sensitif lengkap ke laporan bila lokasi dan
kategorinya sudah cukup untuk investigasi.

## Penanganan

Maintainer akan berupaya:

1. Menghentikan distribusi lanjutan dan menilai dampak.
2. Meminta pemilik sistem merotasi atau mencabut credential yang terdampak.
3. Menghapus data dari branch aktif.
4. Menilai kebutuhan penulisan ulang riwayat Git dan koordinasi dengan GitHub.
5. Memberi tahu pihak yang berwenang sesuai kontrak dan kebijakan yang berlaku.
6. Memperbaiki aturan sanitasi atau validator agar pola serupa lebih mudah
   ditemukan.

Penghapusan dari repositori utama tidak dapat menjamin penghapusan dari fork,
clone, cache, log CI, indeks pencarian, atau salinan pihak lain.

## Dukungan Versi

Hanya versi terbaru pada branch default yang dipelihara. Query memiliki status
kompatibilitas dan pengujian masing-masing dalam `metadata.json`.