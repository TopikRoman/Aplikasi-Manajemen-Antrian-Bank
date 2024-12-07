import csv
import random

class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def delete(self, nomor_rekening):
        current = self.head
        while current:
            if current.data["nomor_rekening"] == nomor_rekening:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def find(self, nomor_rekening):
        current = self.head
        while current:
            if current.data["nomor_rekening"] == nomor_rekening:
                return current.data
            current = current.next
        return None

    def update(self, nomor_rekening, new_data):
        current = self.head
        while current:
            if current.data["nomor_rekening"] == nomor_rekening:
                current.data.update(new_data)
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class BankCRUD:
    def __init__(self, file_name="nasabah.csv"):
        self.file_name = file_name
        self.nasabah_list = DoublyLinkedList()
        self.load_data()

    def generate_nomor_rekening(self):
        return "".join([str(random.randint(0, 9)) for _ in range(16)])

    def load_data(self):
        try:
            with open(self.file_name, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.nasabah_list.append(row)
        except FileNotFoundError:
            with open(self.file_name, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.get_headers())
                writer.writeheader()

    def save_data(self):
        with open(self.file_name, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.get_headers())
            writer.writeheader()
            for data in self.nasabah_list.to_list():
                writer.writerow(data)

    def get_headers(self):
        return ["nama", "no_hp", "no_ktp", "alamat", "nama_ibu", "jenis_kelamin", "setoran_awal", "nomor_rekening"]

    def add_nasabah(self, data):
        data["nomor_rekening"] = self.generate_nomor_rekening()
        self.nasabah_list.append(data)
        self.save_data()
        print("Data nasabah berhasil ditambahkan.")

    def edit_nasabah(self, nomor_rekening, new_data):
        if self.nasabah_list.update(nomor_rekening, new_data):
            self.save_data()
            print("Data nasabah berhasil diperbarui.")
        else:
            print("Nomor rekening tidak ditemukan.")

    def delete_nasabah(self, nomor_rekening):
        if self.nasabah_list.delete(nomor_rekening):
            self.save_data()
            print("Data nasabah berhasil dihapus.")
        else:
            print("Nomor rekening tidak ditemukan.")

    def show_nasabah(self):
        nasabahs = self.nasabah_list.to_list()
        if not nasabahs:
            print("Belum ada data nasabah.")
        else:
            print("\nData Nasabah:")
            for data in nasabahs:
                print(data)
            input()
    def tarik_uang(self, nomor_rekening, jumlah):
        nasabah = self.nasabah_list.find(nomor_rekening)
        if nasabah:
            saldo_sekarang = float(nasabah["setoran_awal"])
            if jumlah > saldo_sekarang:
                print("Saldo tidak mencukupi untuk penarikan.")
            else:
                nasabah["setoran_awal"] = str(saldo_sekarang - jumlah)
                self.save_data()
                print("Penarikan berhasil. Saldo saat ini:", nasabah["setoran_awal"])
        else:
            print("Nomor rekening tidak ditemukan.")

    def setor_uang(self, nomor_rekening, jumlah):
        nasabah = self.nasabah_list.find(nomor_rekening)
        if nasabah:
            saldo_sekarang = float(nasabah["setoran_awal"])
            nasabah["setoran_awal"] = str(saldo_sekarang + jumlah)
            self.save_data()
            print("Setoran berhasil. Saldo saat ini:", nasabah["setoran_awal"])
        else:
            print("Nomor rekening tidak ditemukan.")

def mainMain():
    system = BankCRUD()
    while True:
        print("\nMenu:")
        print("1. Tambah Nasabah")
        print("2. Lihat Data Nasabah")
        print("3. Edit Data Nasabah")
        print("4. Hapus Data Nasabah")
        print("5. Tarik Uang")
        print("6. Setor Uang")
        print("7. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            nama = input("Nama: ")
            no_hp = input("No HP: ")
            no_ktp = input("No KTP: ")
            alamat = input("Alamat: ")
            nama_ibu = input("Nama Ibu: ")
            jenis_kelamin = input("Jenis Kelamin (L/P): ")
            setoran_awal = input("Setoran Awal: ")

            data = {
                "nama": nama,
                "no_hp": no_hp,
                "no_ktp": no_ktp,
                "alamat": alamat,
                "nama_ibu": nama_ibu,
                "jenis_kelamin": jenis_kelamin,
                "setoran_awal": setoran_awal,
            }
            system.add_nasabah(data)

        elif pilihan == "2":
            system.show_nasabah()

        elif pilihan == "3":
            nomor_rekening = input("Masukkan Nomor Rekening: ")
            print("Masukkan data baru (kosongi jika tidak ingin diubah):")
            new_data = {}
            for field in ["nama", "no_hp", "no_ktp", "alamat", "nama_ibu", "jenis_kelamin", "setoran_awal"]:
                value = input(f"{field.capitalize()}: ")
                if value:
                    new_data[field] = value
            system.edit_nasabah(nomor_rekening, new_data)

        elif pilihan == "4":
            nomor_rekening = input("Masukkan Nomor Rekening: ")
            system.delete_nasabah(nomor_rekening)

        elif pilihan == "5":
            nomor_rekening = input("Masukkan Nomor Rekening: ")
            try:
                jumlah = float(input("Masukkan jumlah uang yang ingin ditarik: "))
                system.tarik_uang(nomor_rekening, jumlah)
            except ValueError:
                print("Jumlah harus berupa angka.")

        elif pilihan == "6":
            nomor_rekening = input("Masukkan Nomor Rekening: ")
            try:
                jumlah = float(input("Masukkan jumlah uang yang ingin disetor: "))
                system.setor_uang(nomor_rekening, jumlah)
            except ValueError:
                print("Jumlah harus berupa angka.")

        elif pilihan == "7":
            break
        else:
            print("Pilihan tidak valid.")