import os
import sys
import pwinput
from colorama import Fore, Style, init
from tabulate import tabulate

# Inisialisasi colorama agar warna teks terminal otomatis di-reset
init(autoreset=True)

# Kelas utama yang mengelola sistem Rumah Sakit
class HospitalSystem:
    def __init__(self):
        # Inisialisasi data pengguna (admin, dokter, perawat)
        self.users = {
            "admin1": {"password": "admin123", "role": "admin"},
            "dokter1": {"password": "dokter123", "role": "dokter"},
            "perawat1": {"password": "perawat123", "role": "perawat"}
        }
        # Data pasien awal
        self.patients = {
            1: {"Nama": "Andi", "Usia": 30, "Gender": "L", "Penyakit": "Demam",
                "Kontak": "08123456789", "Alamat": "Jl. Merdeka No. 10",
                "Catatan Medis": ""},
            2: {"Nama": "Budi", "Usia": 25, "Gender": "L", "Penyakit": "Flu",
                "Kontak": "08234567890", "Alamat": "Jl. Sudirman No. 5",
                "Catatan Medis": ""},
            3: {"Nama": "Citra", "Usia": 28, "Gender": "P", "Penyakit": "Sakit Kepala",
                "Kontak": "08345678901", "Alamat": "Jl. Gatot Subroto No. 7",
                "Catatan Medis": ""}
        }
        # Inisialisasi data jadwal konsultasi dan counter ID unik
        self.consultation_schedule = {}
        self.consultation_counter = 1

    # Membersihkan layar terminal sesuai dengan OS yang digunakan
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    # Menampilkan judul halaman dengan format yang konsisten
    def print_title(self, title: str, color=Fore.CYAN):
        self.clear()
        garis = color + Style.BRIGHT + "=" * 60
        print(garis)
        print(color + Style.BRIGHT + "RS. XYZ - Sistem Manajemen Rumah Sakit".center(60))
        print(color + Style.BRIGHT + title.center(60))
        print(garis)

    # Fungsi pause untuk menunggu input dari pengguna sebelum kembali ke menu
    def pause(self):
        input("\nTekan Enter untuk kembali...")

    # Menyaring data pasien sesuai dengan peran pengguna
    def filter_patient_data(self, pid, data, role):
        """
        Menyaring data pasien sesuai peran:
        - Admin & Perawat: dapat melihat Alamat dan Kontak.
        - Dokter & Perawat: dapat melihat Catatan Medis.
        """
        row = {"ID": pid}
        for key, value in data.items():
            if key in ["Alamat", "Kontak"] and role not in ["admin", "perawat"]:
                continue
            if key == "Catatan Medis" and role not in ["dokter", "perawat"]:
                continue
            row[key] = value
        return row

    # Fungsi login untuk mengautentikasi pengguna
    def login(self) -> tuple:
        """
        Menampilkan tampilan login dan mengembalikan (role, username)
        jika login berhasil.
        """
        while True:
            self.print_title("Login Sistem")
            print("1. Masuk\n2. Keluar")
            choice = input("\nPilih menu (1/2): ").strip()
            if choice == "2":
                sys.exit(Fore.YELLOW + "Keluar dari sistem...")
            elif choice == "1":
                username = input("Masukkan Nama Pengguna: ").strip()
                password = pwinput.pwinput("Masukkan Sandi: ").strip()
                user = self.users.get(username)
                if user and user["password"] == password:
                    return user["role"], username
                print(Fore.RED + "\nLogin gagal! Pastikan Nama Pengguna dan Sandi benar.")
                self.pause()
            else:
                print(Fore.RED + "\nPilihan tidak valid! Masukkan 1 atau 2.")
                self.pause()

    # ==================== Manajemen Data Pasien ====================
    # Menampilkan daftar pasien dengan filter sesuai peran
    def view_patients(self, role):
        self.print_title("Daftar Pasien", Fore.YELLOW)
        if not self.patients:
            print(Fore.YELLOW + "Tidak ada data pasien.")
        else:
            table = [self.filter_patient_data(pid, data, role) for pid, data in self.patients.items()]
            print(tabulate(table, headers="keys", tablefmt="fancy_grid"))
        self.pause()

    # Mencari data pasien berdasarkan kata kunci
    def search_patient(self, role):
        self.print_title("Cari Pasien", Fore.BLUE)
        keyword = input("Masukkan kata kunci pencarian: ").strip().lower()
        results = [self.filter_patient_data(pid, data, role)
                   for pid, data in self.patients.items()
                   if keyword in str(pid).lower() or any(keyword in str(v).lower() for v in data.values())]
        if results:
            print(tabulate(results, headers="keys", tablefmt="fancy_grid"))
        else:
            print(Fore.RED + "Pasien tidak ditemukan.")
        self.pause()

    # Menambahkan data pasien baru
    def add_patient(self):
        self.print_title("Tambah Pasien", Fore.RED)
        new_id = max(self.patients.keys()) + 1 if self.patients else 1
        self.patients[new_id] = {
            "Nama": input("Nama: ").strip(),
            "Usia": int(input("Masukkan Usia (angka): ").strip() or "0"),
            "Gender": input("Gender: ").strip(),
            "Penyakit": input("Penyakit: ").strip(),
            "Kontak": input("Kontak: ").strip(),
            "Alamat": input("Alamat: ").strip(),
            "Catatan Medis": input("Catatan Medis: ").strip()
        }
        print(Fore.GREEN + f"Pasien berhasil ditambahkan dengan ID {new_id}!")
        self.pause()

    # Mengubah data pasien yang sudah ada
    def update_patient(self):
        self.print_title("Ubah Data Pasien", Fore.RED)
        self.view_patients("admin")
        try:
            pid = int(input("Masukkan ID pasien (angka): ").strip())
            if pid in self.patients:
                data = self.patients[pid]
                print(Fore.YELLOW + "Masukkan data baru (kosongkan jika tidak ingin mengubah):")
                for key in data:
                    new_val = input(f"{key} ({data[key]}): ").strip()
                    if new_val:
                        data[key] = int(new_val) if key == "Usia" else new_val
                print(Fore.GREEN + "Data pasien diperbarui!")
            else:
                print(Fore.RED + "ID pasien tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

    # Menghapus data pasien berdasarkan ID
    def delete_patient(self):
        self.print_title("Hapus Data Pasien", Fore.RED)
        self.view_patients("admin")
        try:
            pid = int(input("Masukkan ID pasien (angka): ").strip())
            if pid in self.patients:
                del self.patients[pid]
                print(Fore.GREEN + "Data pasien berhasil dihapus!")
            else:
                print(Fore.RED + "ID pasien tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

    # ==================== Fitur Rekam Medis ====================
    # Menambahkan catatan medis untuk pasien
    def add_medical_record(self, doctor):
        self.print_title("Tambah Rekam Medis", Fore.GREEN)
        self.view_patients("dokter")
        try:
            pid = int(input("Masukkan ID pasien (angka): ").strip())
            if pid in self.patients:
                note = input("Masukkan catatan medis: ").strip()
                if note:
                    self.patients[pid]["Catatan Medis"] += f"\n{doctor}: {note}"
                    print(Fore.GREEN + "Rekam medis berhasil ditambahkan!")
                else:
                    print(Fore.YELLOW + "Tidak ada catatan yang ditambahkan.")
            else:
                print(Fore.RED + "ID pasien tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

    # ==================== Fitur Jadwal Konsultasi ====================
    # Menampilkan jadwal konsultasi yang ada (dengan filter sesuai peran)
    def view_consultation_schedule(self, role, user):
        self.print_title("Jadwal Konsultasi", Fore.BLUE)
        if not self.consultation_schedule:
            print(Fore.YELLOW + "Tidak ada jadwal konsultasi.")
        else:
            table = []
            for cid, data in self.consultation_schedule.items():
                # Jika peran dokter, hanya tampilkan jadwal miliknya
                if role == "dokter" and data["Dokter"] != user:
                    continue
                row = {"ID": cid, **data}
                row["Pasien"] = ", ".join(str(x) for x in row["Pasien"]) if data["Pasien"] else "-"
                table.append(row)
            print(tabulate(table, headers="keys", tablefmt="fancy_grid"))
        self.pause()

    # Menambahkan jadwal konsultasi baru
    def add_consultation_schedule(self, role, user):
        self.print_title("Tambah Jadwal Konsultasi", Fore.GREEN)
        if role not in ["admin", "dokter"]:
            print(Fore.RED + "Akses ditolak!")
            self.pause()
            return
        tanggal = input("Masukkan tanggal konsultasi (YYYY-MM-DD): ").strip()
        waktu = input("Masukkan waktu konsultasi (misal: 10:00 - 12:00): ").strip()
        deskripsi = input("Masukkan deskripsi/judul: ").strip()
        dokter = user if role == "dokter" else input("Masukkan nama dokter: ").strip()
        self.consultation_schedule[self.consultation_counter] = {
            "Dokter": dokter, "Tanggal": tanggal, "Waktu": waktu,
            "Deskripsi": deskripsi, "Pasien": []
        }
        print(Fore.GREEN + f"Jadwal konsultasi berhasil ditambahkan dengan ID {self.consultation_counter}!")
        self.consultation_counter += 1
        self.pause()

    # Mengubah data jadwal konsultasi
    def update_consultation_schedule(self, role, user):
        self.print_title("Ubah Jadwal Konsultasi", Fore.GREEN)
        try:
            cid = int(input("Masukkan ID jadwal konsultasi (angka): ").strip())
            if cid in self.consultation_schedule:
                if role == "dokter" and self.consultation_schedule[cid]["Dokter"] != user:
                    print(Fore.RED + "Akses ditolak! Anda hanya dapat mengubah jadwal Anda sendiri.")
                else:
                    for key in ["Tanggal", "Waktu", "Deskripsi"]:
                        new_val = input(f"{key} (sebelumnya: {self.consultation_schedule[cid][key]}): ").strip()
                        if new_val:
                            self.consultation_schedule[cid][key] = new_val
                    print(Fore.GREEN + "Jadwal konsultasi berhasil diperbarui!")
            else:
                print(Fore.RED + "ID jadwal konsultasi tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

    # Menghapus jadwal konsultasi berdasarkan ID
    def delete_consultation_schedule(self, role, user):
        self.print_title("Hapus Jadwal Konsultasi", Fore.RED)
        try:
            cid = int(input("Masukkan ID jadwal konsultasi (angka): ").strip())
            if cid in self.consultation_schedule:
                if role == "dokter" and self.consultation_schedule[cid]["Dokter"] != user:
                    print(Fore.RED + "Akses ditolak! Anda hanya dapat menghapus jadwal Anda sendiri.")
                else:
                    del self.consultation_schedule[cid]
                    print(Fore.GREEN + "Jadwal konsultasi berhasil dihapus!")
            else:
                print(Fore.RED + "ID jadwal konsultasi tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

    # Menambahkan pasien ke dalam jadwal konsultasi tertentu
    def add_patient_to_consultation(self, role, user):
        self.print_title("Tambah Pasien ke Jadwal Konsultasi", Fore.GREEN)
        if role not in ["admin", "dokter"]:
            print(Fore.RED + "Akses ditolak!")
            self.pause()
            return
        try:
            cid = int(input("Masukkan ID jadwal konsultasi (angka): ").strip())
            if cid in self.consultation_schedule:
                if role == "dokter" and self.consultation_schedule[cid]["Dokter"] != user:
                    print(Fore.RED + "Akses ditolak! Anda hanya dapat menambahkan pasien ke jadwal Anda sendiri.")
                else:
                    pid = int(input("Masukkan ID pasien (angka): ").strip())
                    if pid in self.patients:
                        if pid not in self.consultation_schedule[cid]["Pasien"]:
                            self.consultation_schedule[cid]["Pasien"].append(pid)
                            print(Fore.GREEN + f"Pasien dengan ID {pid} berhasil ditambahkan ke jadwal konsultasi {cid}!")
                        else:
                            print(Fore.YELLOW + "Pasien sudah terdaftar pada jadwal tersebut.")
                    else:
                        print(Fore.RED + "ID pasien tidak ditemukan!")
            else:
                print(Fore.RED + "ID jadwal konsultasi tidak ditemukan!")
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
        self.pause()

# ==================== Menu Berdasarkan Peran ====================
# Menu untuk admin dengan akses penuh terhadap data pasien dan jadwal konsultasi
def admin_menu(system, user):
    while True:
        system.print_title("Menu Admin", Fore.CYAN)
        print("1. Manajemen Pasien & Rekam Medis")
        print("2. Kelola Jadwal Konsultasi")
        print("0. Logout")
        c = input("\nPilih menu (angka): ").strip()
        if c == "1":
            while True:
                system.print_title("Manajemen Pasien & Rekam Medis", Fore.GREEN)
                print("1. Lihat Pasien")
                print("2. Cari Pasien")
                print("3. Tambah Pasien")
                print("4. Ubah Data Pasien")
                print("5. Hapus Pasien")
                print("6. Tambah Rekam Medis")
                print("0. Kembali")
                sub = input("\nPilih menu (angka): ").strip()
                if sub == "1":
                    system.view_patients("admin")
                elif sub == "2":
                    system.search_patient("admin")
                elif sub == "3":
                    system.add_patient()
                elif sub == "4":
                    system.update_patient()
                elif sub == "5":
                    system.delete_patient()
                elif sub == "6":
                    system.add_medical_record(user)
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "Pilihan tidak valid!")
                    system.pause()
        elif c == "2":
            while True:
                system.print_title("Kelola Jadwal Konsultasi", Fore.BLUE)
                print("1. Lihat Jadwal Konsultasi")
                print("2. Tambah Jadwal Konsultasi")
                print("3. Ubah Jadwal Konsultasi")
                print("4. Hapus Jadwal Konsultasi")
                print("5. Tambah Pasien ke Jadwal Konsultasi")
                print("0. Kembali")
                sub = input("\nPilih menu (angka): ").strip()
                if sub == "1":
                    system.view_consultation_schedule("admin", user)
                elif sub == "2":
                    system.add_consultation_schedule("admin", user)
                elif sub == "3":
                    system.update_consultation_schedule("admin", user)
                elif sub == "4":
                    system.delete_consultation_schedule("admin", user)
                elif sub == "5":
                    system.add_patient_to_consultation("admin", user)
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "Pilihan tidak valid!")
                    system.pause()
        elif c == "0":
            print(Fore.YELLOW + "\nLogout berhasil!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            system.pause()

# Menu untuk dokter dengan akses terbatas pada fitur tertentu
def dokter_menu(system, user):
    while True:
        system.print_title("Menu Dokter", Fore.CYAN)
        print("1. Manajemen Pasien & Rekam Medis")
        print("2. Kelola Jadwal Konsultasi")
        print("0. Logout")
        c = input("\nPilih menu (angka): ").strip()
        if c == "1":
            while True:
                system.print_title("Manajemen Pasien & Rekam Medis", Fore.GREEN)
                print("1. Lihat Pasien")
                print("2. Cari Pasien")
                print("3. Tambah Rekam Medis")
                print("0. Kembali")
                sub = input("\nPilih menu (angka): ").strip()
                if sub == "1":
                    system.view_patients("dokter")
                elif sub == "2":
                    system.search_patient("dokter")
                elif sub == "3":
                    system.add_medical_record(user)
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "Pilihan tidak valid!")
                    system.pause()
        elif c == "2":
            while True:
                system.print_title("Kelola Jadwal Konsultasi", Fore.BLUE)
                print("1. Lihat Jadwal Konsultasi")
                print("2. Tambah Jadwal Konsultasi")
                print("3. Ubah Jadwal Konsultasi")
                print("4. Hapus Jadwal Konsultasi")
                print("5. Tambah Pasien ke Jadwal Konsultasi")
                print("0. Kembali")
                sub = input("\nPilih menu (angka): ").strip()
                if sub == "1":
                    system.view_consultation_schedule("dokter", user)
                elif sub == "2":
                    system.add_consultation_schedule("dokter", user)
                elif sub == "3":
                    system.update_consultation_schedule("dokter", user)
                elif sub == "4":
                    system.delete_consultation_schedule("dokter", user)
                elif sub == "5":
                    system.add_patient_to_consultation("dokter", user)
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "Pilihan tidak valid!")
                    system.pause()
        elif c == "0":
            print(Fore.YELLOW + "\nLogout berhasil!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            system.pause()

# Menu untuk perawat dengan akses terbatas (tidak bisa tambah atau ubah data pasien)
def perawat_menu(system, user):
    while True:
        system.print_title("Menu Perawat", Fore.CYAN)
        print("1. Manajemen Pasien")
        print("2. Lihat Jadwal Konsultasi")
        print("0. Logout")
        c = input("\nPilih menu (angka): ").strip()
        if c == "1":
            while True:
                system.print_title("Manajemen Pasien", Fore.GREEN)
                print("1. Lihat Pasien")
                print("2. Cari Pasien")
                print("0. Kembali")
                sub = input("\nPilih menu (angka): ").strip()
                if sub == "1":
                    system.view_patients("perawat")
                elif sub == "2":
                    system.search_patient("perawat")
                elif sub == "0":
                    break
                else:
                    print(Fore.RED + "Pilihan tidak valid!")
                    system.pause()
        elif c == "2":
            system.view_consultation_schedule("perawat", user)
        elif c == "0":
            print(Fore.YELLOW + "\nLogout berhasil!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            system.pause()

# Fungsi utama untuk menjalankan aplikasi
def main():
    # Inisialisasi sistem
    system = HospitalSystem()
    while True:
        role, user = system.login()
        if role == "admin":
            admin_menu(system, user)
        elif role == "dokter":
            dokter_menu(system, user)
        elif role == "perawat":
            perawat_menu(system, user)

if __name__ == "__main__":
    main()
