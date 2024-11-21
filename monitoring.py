import psutil
import time
import os

def clear_screen():
    """Ekrani temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')

def system_monitor():
    while True:
        clear_screen()

        # CPU Kullanimi
        print(f"CPU Kullanimi: {psutil.cpu_percent(interval=1)}%")
        print(f"Her bir çekirdek kullanimi: {psutil.cpu_percent(interval=1, percpu=True)}")

        # RAM Kullanimi
        memory = psutil.virtual_memory()
        print(f"RAM Kullanimi: {memory.percent}%")
        print(f"Kullanilan RAM: {memory.used / (1024 ** 3):.2f} GB")
        print(f"Toplam RAM: {memory.total / (1024 ** 3):.2f} GB")

        # Disk Kullanimi
        disk = psutil.disk_usage('/')
        print(f"Disk Kullanimi: {disk.percent}%")
        print(f"Kullanilan Disk: {disk.used / (1024 ** 3):.2f} GB")
        print(f"Toplam Disk: {disk.total / (1024 ** 3):.2f} GB")

        # Ağ Bilgileri
        net = psutil.net_io_counters()
        print(f"Toplam Gönderilen: {net.bytes_sent / (1024 ** 2):.2f} MB")
        print(f"Toplam Alinan: {net.bytes_recv / (1024 ** 2):.2f} MB")

        # İşlemler ve Çekirdek Bilgisi
        print(f"Toplam Çekirdek Sayisi: {psutil.cpu_count(logical=False)}")
        print(f"Toplam Mantiksal İşlemci: {psutil.cpu_count(logical=True)}")

        # 2 saniye bekle
        time.sleep(5)

if __name__ == "__main__":
    try:
        system_monitor()
    except KeyboardInterrupt:
        print("\nSistem monitörü kapatildi.")