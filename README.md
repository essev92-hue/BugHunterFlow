# 🐛 BugHunterFlow - Tools Bug Hunting Otomatis untuk Pemula

![Easy to Use](https://img.shields.io/badge/Untuk-Pemula-green)
![Bahasa Indonesia](https://img.shields.io/badge/Bahasa-Indonesia-blue)
![One Command](https://img.shields.io/badge/Satu_Perintah-Selesai-orange)

**BugHunterFlow** adalah tools otomatis yang mencari bug/vulnerability di website. Cukup jalankan satu perintah, dapatkan hasil lengkap! ✨

---

## 🚀 **INSTALASI CEPAT (Copy Paste Saja!)**

### **LANGKAH 1: Install Dasar (5 Menit)**
```bash
# Salin SEMUA baris ini ke terminal (Ctrl+Shift+V)

# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python dan tools dasar
sudo apt install -y python3 python3-pip git curl wget nmap jq

# Install Go
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### **LANGKAH 2: Download BugHunterFlow**
```bash
# Download tools
git clone https://github.com/essev92-hue/BugHunterFlow.git

# Masuk ke folder
cd BugHunterFlow

# Beri permission
chmod +x *.sh *.py
```

### **LANGKAH 3: Install Python Packages**
```bash
pip3 install requests beautifulsoup4 urllib3
```

---

## 🎯 **CARA MENJALANKAN (SANGAT MUDAH!)**

### **PILIH SALAH SATU:**
```bash
# 🟢 PILIHAN 1: Website test (AMAN untuk pemula)
./bughunter.sh testphp.vulnweb.com

# 🟡 PILIHAN 2: Website demo
./bughunter.sh scanme.nmap.org

# 🔵 PILIHAN 3: Website Anda sendiri
./bughunter.sh website-anda.com
```

### **TUNGGU 5-10 MENIT** sambil minum kopi ☕

---

## 📊 **HASIL AKAN MUNCUL DI:**

Setelah selesai, buka folder `output/`:
```bash
# Lihat hasil scan
cd output/
ls -la

# Contoh: Jika scan testphp.vulnweb.com
cd testphp.vulnweb.com/
ls -la
```

### **File Hasil yang Didapat:**
```
📁 output/testphp.vulnweb.com/
├── 📄 web_tech.json          → Teknologi yang dipakai website
├── 📄 endpoints.txt          → Link tersembunyi
├── 📄 parameters.txt         → Parameter website
├── 📄 bug_findings.json      → Bug yang ditemukan
├── 📄 security_report.md     → Analisis keamanan
└── 📄 js_analysis.txt       → Rahasia di JavaScript
```

---

## 🐛 **JENIS BUG YANG BISA DITEMUKAN:**

| Bug | Artinya | Contoh |
|-----|---------|---------|
| **XSS** | Bisa inject script jahat | `<script>alert(1)</script>` |
| **SQL Injection** | Bisa akses database | `' OR '1'='1` |
| **IDOR** | Bisa lihat data orang | `user_id=123` → `user_id=124` |
| **SSRF** | Bisa akses server internal | `url=http://localhost` |
| **RCE** | Bisa jalankan perintah | `; ls -la` |

---

## ⚠️ **PERINGATAN PENTING!**

### **✅ BOLEH DI-TEST:**
```bash
# Website legal untuk testing
./bughunter.sh testphp.vulnweb.com
./bughunter.sh bodgeit.herokuapp.com
./bughunter.sh demo.testfire.net
```

### **❌ JANGAN DI-TEST:**
- Website perusahaan/orang lain
- Website pemerintah
- Website tanpa izin
- Website live/produksi

**🚫 TEST TANPA IZIN = ILEGAL!**

---
## ⚠️ DISCLAIMER & ETIKA PENGGUNAAN

Tools ini dibuat untuk tujuan:
- Pendidikan dan pembelajaran keamanan siber
- Testing sistem yang ANDA MILIKI
- Bug bounty dengan izin eksplisit
- Penelitian keamanan yang legal

### PERINGATAN:
1. **JANGAN** gunakan untuk hacking ilegal
2. **JANGAN** test website tanpa izin
3. **JANGAN** gunakan untuk kejahatan siber
4. **HANYA** gunakan di lingkungan yang Anda kuasai

### TANGGUNG JAWAB:
Penulis TIDAK bertanggung jawab atas:
- Penyalahgunaan tools ini
- Kerusakan sistem pihak lain
- Konsekuensi hukum dari penggunaan ilegal
- Kehilangan data atau kerugian finansial

### ETIKA HACKING:
1. Always get permission
2. Respect privacy
3. Don't destroy data
4. Report vulnerabilities responsibly
5. Help improve security

**"With great power comes great responsibility"**
## 🔧 **SOLUSI MASALAH UMUM:**

### **Masalah: "bash: ./bughunter.sh: Permission denied"**
```bash
chmod +x bughunter.sh
```

### **Masalah: "command not found: subfinder"**
```bash
# Install tools Go
cat > install_tools.sh << 'EOF'
#!/bin/bash
echo "[+] Installing tools..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install -v github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/ffuf/ffuf@latest
EOF

chmod +x install_tools.sh
./install_tools.sh
export PATH="$PATH:$HOME/go/bin"
```

### **Masalah: "ModuleNotFoundError: No module named 'requests'"**
```bash
pip3 install requests beautifulsoup4 --user
```

### **Masalah: Scan terlalu lama**
```bash
# Tekan Ctrl+C untuk stop
# Coba website yang lebih kecil
./bughunter.sh example.com
```

---

## 📖 **TUTORIAL LENGKAP:**

### **Video Tutorial:**
- [Video Install](https://youtube.com) *(coming soon)*
- [Video Cara Pakai](https://youtube.com) *(coming soon)*
- [Video Baca Hasil](https://youtube.com) *(coming soon)*

### **Langkah-demi-Langkah:**
1. **Install** → Copy paste command di atas
2. **Jalankan** → `./bughunter.sh target.com`
3. **Tunggu** → 5-10 menit
4. **Cek Hasil** → Lihat folder `output/`
5. **Pelajari** → Baca file hasil

---

## 🤔 **PERTANYAAN UMUM (FAQ):**

### **Q: Saya pemula banget, bisa pakai?**
**A:** BISA! Cukup copy paste command di atas.

### **Q: Butuh waktu berapa lama?**
**A:** 5-15 menit untuk website kecil.

### **Q: Butuh komputer canggih?**
**A:** Tidak, laptop biasa bisa jalan.

### **Q: Hasilnya gimana bentuknya?**
**A:** File teks biasa, bisa dibuka di Notepad.

### **Q: Aman buat pemula?**
**A:** Aman, asal test website yang diizinkan.

### **Q: Kalau error gimana?**
**A:** Lihat bagian "Solusi Masalah Umum" di atas.

---

## 🎮 **CHALLENGE UNTUK PEMULA:**

### **Level 1: Pemula**
```bash
./bughunter.sh testphp.vulnweb.com
```
**Tugas:** Cari minimal 1 bug XSS

### **Level 2: Menengah**
```bash
./bughunter.sh bodgeit.herokuapp.com
```
**Tugas:** Cari SQL Injection

### **Level 3: Lanjutan**
```bash
./bughunter.sh website-anda-sendiri.com
```
**Tugas:** Perbaiki semua bug yang ditemukan

---

## 📝 **CONTOH HASIL NYATA:**

```json
// web_tech.json
{
  "technologies": [
    {"type": "Server", "name": "Apache/2.4.41"},
    {"type": "Framework", "name": "WordPress"},
    {"type": "Database", "name": "MySQL"}
  ]
}

// bug_findings.json
{
  "xss": [
    {
      "url": "http://target.com/search?q=<script>alert(1)</script>",
      "payload": "<script>alert(1)</script>"
    }
  ],
  "sqli": [
    {
      "url": "http://target.com/user?id=1'",
      "note": "Potential SQL Injection"
    }
  ]
}
```

---

## 🛠️ **FITUR UNGGULAN:**

✅ **Otomatis** - Satu perintah, semua jalan  
✅ **Lengkap** - 6 fase scanning komplit  
✅ **Mudah** - Hasil dalam file teks  
✅ **Cepat** - 5-15 menit per website  
✅ **Legal** - Test hanya yang diizinkan  
✅ **Gratis** - 100% free dan open source  

---

## 👥 **KOMUNITAS & BANTUAN:**

### **Jika stuck:**
1. **Baca FAQ** di atas
2. **Cek error message**
3. **Google error tersebut**
4. **Buat issue di GitHub**

### **Link Penting:**
- 📚 **Dokumentasi Lengkap**: [GitHub Wiki](https://github.com/essev92-1/BugHunterFlow/wiki)
- 🐛 **Report Bug**: [Issues](https://github.com/essev92-1/BugHunterFlow/issues)
- 💬 **Diskusi**: [Discussions](https://github.com/essev92-1/BugHunterFlow/discussions)
- ⭐ **Support**: Star repository ini!

---

## ⭐ **CARANYA DUKUNG PROJECT INI:**

**Gratis tapi butuh support kalian:**
1. **⭐ Give Star** di GitHub
2. **🔗 Share** ke teman
3. **🐛 Report** bug jika ketemu
4. **💡 Suggest** fitur baru

---

## 🎁 **BONUS: SCRIPT INSTALL ALL-IN-ONE**

```bash
# SALIN SEMUA BARIS INI UNTUK INSTALL OTOMATIS:

#!/bin/bash
echo "[+] Installing BugHunterFlow..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git curl wget nmap jq
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc
git clone https://github.com/essev92-1/BugHunterFlow.git
cd BugHunterFlow
chmod +x *.sh *.py
pip3 install requests beautifulsoup4 urllib3
echo "[+] Installation Selesai!"
echo "[+] Jalankan: ./bughunter.sh testphp.vulnweb.com"
```

---

## 📞 **NEED HELP?**

**Masih bingung? Coba ini:**
```bash
# Jalankan test mini
cd BugHunterFlow
python3 web_tech.py testphp.vulnweb.com
cat output/testphp.vulnweb.com/web_tech.json
```

**Atau kontak:**
- 📧 Email: (tambahkan email Anda)
- 💬 Discord: (tambahkan link Discord)
- 🐦 Twitter: (tambahkan Twitter)

---

## 🏆 **CREDITS**

Dibuat dengan ❤️ oleh **@essev92-1**  
Untuk komunitas bug hunter Indonesia  
"Belajar security harus mudah dan menyenangkan!"

---

## 📄 **LICENSE**

MIT License - Bebas pakai, modifikasi, dan distribusi  
**Tapi tetap bertanggung jawab ya!** 🙏

---

**✨ SELAMAT! Anda sekarang punya tools bug hunting profesional!**

**⚠️ INGAT: Gunakan untuk kebaikan, bukan kejahatan!**

**Happy Hunting! 🐛🔍**  

*"The best way to learn is by doing"*
