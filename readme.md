# Proyek Mini Program: Master Congklak (AI Challenge)

Dokumentasi ini berisi panduan lengkap untuk menginstal dan menjalankan aplikasi permainan Congklak (Mancala) melawan AI.

---

## 1. Library yang Digunakan

Proyek ini dibangun menggunakan beberapa library, baik yang perlu diinstal maupun yang sudah menjadi bagian dari Python.

* **Pygame (Eksternal)**: Ini adalah library utama yang harus diinstal. Pygame digunakan untuk membuat seluruh antarmuka grafis (GUI), menggambar papan, biji, tombol, menangani input mouse/keyboard, dan mengelola *game loop*.
* **Math (Bawaan Python)**: Digunakan untuk kalkulasi, seperti `math.inf` (logika AI), `math.hypot` (deteksi klik mouse), dan `math.sin`/`math.cos` (efek visual).
* **Random (Bawaan Python)**: Digunakan untuk memposisikan biji secara acak di lubang dan untuk AI memilih langkah jika ada opsi yang sama baiknya.
* **Sys (Bawaan Python)**: Digunakan untuk keluar dari aplikasi dengan benar (`sys.exit()`).
* **Time (Bawaan Python)**: Digunakan untuk memberi jeda, mengatur animasi, dan mengontrol kecepatan game (FPS).

---

## 2. IDE Pengembangan

Aplikasi ini dikembangkan menggunakan *Integrated Development Environment* (IDE):

* **[Silakan isi dengan nama IDE Anda, contoh: Visual Studio Code, PyCharm, Sublime Text, atau IDLE]**

---

## 3. Langkah Detail Instalasi dan Penggunaan

Ini adalah panduan langkah demi langkah untuk menjalankan game ini di komputer baru yang belum memiliki Python.

### Bagian A: Instalasi Python (Fondasi Utama)

Game ini ditulis dalam bahasa Python. Kita harus menginstal "penerjemah" Python terlebih dahulu.

1.  **Unduh Python**:
    Buka browser web Anda (seperti Google Chrome atau Edge) dan kunjungi situs web resmi Python:
    [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Jalankan Installer**:
    Klik tombol "Download Python" (biasanya versi terbaru seperti 3.11 atau 3.12). Setelah file `.exe` selesai diunduh, klik dua kali untuk membukanya.

3.  **PENTING: "Add to PATH"**:
    Di layar instalasi pertama, akan ada kotak centang di bagian bawah layar. **Pastikan Anda mencentang kotak yang bertuliskan "Add Python to PATH"** atau "Add python.exe to PATH". Ini sangat penting agar komputer Anda dapat menemukan Python dari mana saja.

4.  **Instalasi**:
    Setelah mencentang kotak "Add to PATH", klik **"Install Now"**. Tunggu prosesnya hingga selesai.

5.  **Verifikasi (Opsional tapi Disarankan)**:
    Untuk memastikan Python terinstal, buka **Terminal** atau **Command Prompt (CMD)** (cari di Start Menu). Ketik perintah berikut dan tekan Enter:
    ```bash
    python --version
    ```
    Jika instalasi berhasil, Anda akan melihat versi Python yang baru saja Anda instal (misal: `Python 3.12.0`). Tutup terminal ini.

### Bagian B: Dapatkan File Proyek

Anda perlu mendapatkan kedua file kode (`ai.py` dan `game.py`) ke komputer Anda.

1.  **Unduh Proyek (Cara Utama)**:
    * Kunjungi link berikut untuk mengunduh file proyek.
        *(Ini mungkin akan mengunduh file `.zip` yang berisi semua kode).*

    * **LINK DOWNLOAD:**
        **[!!! MASUKKAN LINK DOWNLOAD ANDA DI SINI !!!]**
        *(Contoh: Link ke Google Drive, GitHub, WeTransfer, dll.)*

2.  **Ekstrak File (Jika .zip)**:
    * Setelah file `.zip` terunduh, temukan file tersebut di folder `Downloads` Anda.
    * Klik kanan pada file `.zip` tersebut dan pilih **"Extract All..."** atau **"Ekstrak Semua..."**.
    * Pilih lokasi yang mudah diingat (misalnya `Documents` atau `Desktop`) untuk menyimpan file-filenya. Ini akan membuat folder baru (contoh: `Proyek-Congklak-main`).

3.  **Pastikan File Lengkap**:
    * Buka folder yang baru saja Anda ekstrak.
    * Pastikan Anda melihat kedua file ini di dalamnya:
        * `ai.py`
        * `mancala.py`

### Bagian C: Instalasi Library (Pygame)

Sekarang kita perlu menginstal "bahan" Pygame yang dibutuhkan oleh game Anda.

1.  **Buka Terminal di Folder Proyek**:
    Ini adalah cara termudah. Buka folder proyek yang sudah Anda ekstrak tadi (yang berisi `ai.py` dan `game.py`). Di bagian yang kosong (jangan klik file), **Klik Kanan** (di Windows 11) atau **Shift + Klik Kanan** (di Windows 10), lalu pilih:
    **"Buka di Terminal"** atau **"Open in Terminal"** atau **"Open PowerShell window here"**.

2.  **(Alternatif) Jika Langkah 1 Gagal**:
    Buka Terminal/CMD secara manual (dari Start Menu). Anda harus "pindah" ke folder proyek Anda. Gunakan perintah `cd` (change directory). Contoh:
    ```bash
    # Ganti "NamaAnda" dan nama folder Anda sesuai jalur di komputer Anda
    cd C:\Users\NamaAnda\Documents\Proyek-Congklak-main
    ```

3.  **Instal Pygame**:
    Setelah terminal Anda "berada" di dalam folder yang benar, ketik perintah berikut dan tekan Enter:
    ```bash
    pip install pygame
    ```
    * `pip` adalah manajer paket Python (sudah terinstal bersama Python). Perintah ini berarti "Tolong ambil dan instal library Pygame".

4.  **Tunggu**:
    Tunggu beberapa saat hingga terminal menampilkan pesan "Successfully installed pygame...".

### Bagian D: Menjalankan Game!

Setelah semua persiapan selesai, Anda siap bermain.

1.  **Pastikan Terminal Masih Terbuka**:
    Pastikan jendela Terminal/CMD Anda masih terbuka dan berada di dalam folder proyek (Anda akan melihat nama folder Anda di *prompt*, misal `C:\... \Proyek-Congklak-main>`).

2.  **Jalankan File Utama**:
    Ketik perintah berikut untuk menjalankan file game utama (`game.py`). Tekan Enter.
    ```bash
    python game.py
    ```

3.  **Selesai**:
    Jendela permainan "Master Congklak" akan terbuka di layar Anda. Selamat bermain!