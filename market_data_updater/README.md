# Open Low Strategy

Pre-requisite:
- Punya akun Stockbit Sekuritas
- Buat file `users.py` dan isi dengan format: `list = ["email", "password", "pin"]`
- Buat task scheduler yg akan menjalankan aplikasi ini pada jam 09:01

How it works:
- Sistem akan melakukan scanning market jam 09:01 WIB
- Proses scanning berjalan sekitar ~20 detik
- Ketika saham yg memenuhi kriteria open == low ditemukan maka akan langsung melakukan buy HAKA
- Lalu sistem akan mengecek apakah pembelian berhasil
- Jika berhasil maka akan melakukan order sell di harga = buy price +3 tick
