## File untuk NPM dan Password

Buat file bernama `login_detail.txt`

Pastikan file ini mengikuti format di bawah ini:

| Nama       | Deskripsi                  |
| ---------- | -------------------------- |
| `npm`      | Nomor Induk Mahasiswa Anda |
| `password` | Password akun Anda         |

## Koneksi ke telegram

Buat file bernama `telegram_api.txt`

| Format               |
| -------------------- |
| `api_id=`            |
| `api_hash=`          |
| `phone=`             |
| `receiver_username=` |

note :

`api_id` dan `api_hash` register https://my.telegram.org/apps

`phone` nomor telepon telegram yang di daftarkan

`receiver_username` username telegram yang akan menerima pesan

## Buat venv

`python3 -m venv .env`

activate venv :
`source .env/bin/activate`

deactivate :
`deactivated`

# How Run Automation

Auto absensi `python main.py`

Untuk mendapatkan link dari semua materi pertemuan yang tersedia `python materi.py`

![GitHub](https://img.shields.io/github/languages/top/username/repository?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-brightgreen)
