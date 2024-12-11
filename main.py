from adminbank import mainMain, BankCRUD
import os

class Node:
  def __init__(self, data=None):
    self.data = data
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = None

  def append(self, data):
    new_node = Node(data)
    if not self.head:
      self.head = new_node
      return
    last = self.head
    while last.next:
      last = last.next
    last.next = new_node

  def display(self):
    elems = []
    current = self.head
    while current:
      elems.append(current.data)
      current = current.next
    return elems

class Queue:
  def __init__(self):
    self.queue = LinkedList()

  def enqueue(self, data):
    self.queue.append(data)

  def dequeue(self):
    if self.queue.head is None:
      return None
    dequeued_data = self.queue.head.data
    self.queue.head = self.queue.head.next
    return dequeued_data

  def display(self):
    return self.queue.display()

  def lihat_nomor_berikutnya(self):
    if self.queue.head is None:
      return None
    return self.queue.head.data

class BankQueueSystem:
  def __init__(self):
    self.queue = Queue()
    self.admin_passwords = {"Teller 1": "admin123", "Teller 2": "admin456"}
    self.nasabah_data = {}

  def nasabah_ambil_nomor(self, nama):
    nomor_antrian = len(self.queue.display()) + 1
    self.queue.enqueue(nomor_antrian)
    self.nasabah_data[nomor_antrian] = nama
    print(f"Nomor antrian Anda adalah: {nomor_antrian}")
    input()

  def admin_login(self, teller, password):
    return self.admin_passwords.get(teller) == password

  def admin_lihat_antrian(self):
    antrian = self.queue.display()
    if not antrian:
      os.system("cls")
      print("Tidak ada antrian.")
    else:
      os.system("cls")
      print("Antrian saat ini:", antrian)
    input()

  def admin_panggil_antrian(self, teller):
    nomor_dipanggil = self.queue.dequeue()
    if nomor_dipanggil is None:
      print("Tidak ada antrian yang dipanggil.")
      input()
    else:
      os.system("cls")
      nama = self.nasabah_data.pop(nomor_dipanggil, "Tidak diketahui")
      print(f"Panggilan Nomor antrian {nomor_dipanggil}, silahkan ke {teller}. Nama: {nama}")
      next_queue = self.queue.display()
      if next_queue:
        print(f"Nomor antrian berikutnya: {next_queue[0]}")
      else:
        print("Tidak ada antrian berikutnya.")
      input()
      mainMain()

def main():
  system = BankQueueSystem()
  system2 = BankCRUD()
  while True:
    os.system("cls")
    print("\n1. Nasabah Ambil Nomor")
    print("2. Admin Login")
    print("3. Keluar")
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
      nama = input("Masukkan nama Anda: ")
      system.nasabah_ambil_nomor(nama)
    elif pilihan == "2":
      teller = input("Masukkan teller (Teller 1/Teller 2): ")
      password = input(f"Masukkan password admin {teller}: ")
      if system.admin_login(teller, password):
        while True:
          os.system("cls")
          print(f"\nAdmin {teller} Menu:")
          print("1. Lihat Antrian")
          print("2. Panggil Antrian")
          print("3. Tampilkan Data Nasabah")
          print("4. Logout")
          admin_pilihan = input("Pilih menu admin: ")

          if admin_pilihan == "1":
            system.admin_lihat_antrian()
          elif admin_pilihan == "2":
            system.admin_panggil_antrian(teller)
          elif admin_pilihan == "3":
            os.system('cls')
            system2.show_nasabah()
          elif admin_pilihan == "4":
            break
          else:
            print("Pilihan tidak valid.")
      else:
        print("Password salah.")
    elif pilihan == "3":
      break
    else:
      print("Pilihan tidak valid.")

if __name__ == "__main__":
  main()

