import sys
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QScrollArea
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Performance Monitor")
        self.setGeometry(100, 100, 600, 800)

        # Main Widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignTop)

        # Labels for CPU, RAM, Disk Usage
        self.cpu_label = QLabel(self)
        self.ram_label = QLabel(self)
        self.disk_label = QLabel(self)

        # Open Files Display
        self.open_files_label = QLabel("Açık Dosyalar ve Processler:")
        self.open_files_text = QTextEdit(self)
        self.open_files_text.setReadOnly(True)

        # Set font and style for labels
        font = QFont("Arial", 14, QFont.Bold)
        self.cpu_label.setFont(font)
        self.ram_label.setFont(font)
        self.disk_label.setFont(font)
        self.open_files_label.setFont(font)

        # Set color palette for labels
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.cpu_label.setPalette(palette)
        self.ram_label.setPalette(palette)
        self.disk_label.setPalette(palette)
        self.open_files_label.setPalette(palette)

        # Widgetları arayüze ekliyoru
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.open_files_label)
        self.layout.addWidget(self.open_files_text)

        self.setStyleSheet("background-color: #FFFFFF;")

        # Veriler anında güncellenmemesi için 10 saniye gecikme bırakıyorum.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(10000)  # 10 Saniyede bir güncellenecek.

        # Initial update
        self.update_metrics()

    def update_metrics(self):

        # Get system performance metrics
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        disk_free = psutil.disk_usage('/').free / 1024 ** 3

        self.cpu_label.setText(f"CPU Kullanımı: {cpu_usage}%")
        self.ram_label.setText(f"Bellek Kullanımı: {ram_usage}%")
        self.disk_label.setText(f"Disk Kullanımı: {disk_usage}%, {disk_free:.2f} GB Boş")

        open_files = self.get_open_files_info()
        self.open_files_text.setText(open_files)

#Processleri ve açık dosyaları tek bir fonksiyon içinde topluyoruz.
    def get_open_files_info(self):
        open_files_list = []
        for proc in psutil.process_iter(['pid','name']):
            try:
                files = proc.open_files()
                if files:
                    open_files_list.append(f"Process ID: {proc.info['pid']} | Process İsmi: {proc.info['name']} | Açık Dosyalar:\n")
                    for file in files:
                        open_files_list.append(f"    {file.path}")
                    open_files_list.append("\n**********************************************************************************")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return "\n".join(open_files_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
