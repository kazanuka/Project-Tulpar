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

        # Processes Display
        self.processes_label = QLabel("Processes:")
        self.processes_text = QTextEdit(self)
        self.processes_text.setReadOnly(True)

        # Open Files Display
        self.open_files_label = QLabel("Open Files:")
        self.open_files_text = QTextEdit(self)
        self.open_files_text.setReadOnly(True)

        # Set font and style for labels
        font = QFont("Arial", 14, QFont.Bold)
        self.cpu_label.setFont(font)
        self.ram_label.setFont(font)
        self.disk_label.setFont(font)
        self.processes_label.setFont(font)
        self.open_files_label.setFont(font)

        # Set color palette for labels
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.cpu_label.setPalette(palette)
        self.ram_label.setPalette(palette)
        self.disk_label.setPalette(palette)
        self.processes_label.setPalette(palette)
        self.open_files_label.setPalette(palette)

        # Add widgets to layout
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.processes_label)
        self.layout.addWidget(self.processes_text)
        self.layout.addWidget(self.open_files_label)
        self.layout.addWidget(self.open_files_text)

        # Set background color
        self.setStyleSheet("background-color: #FFFFFFF;")

        # Timer to update the metrics
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(10000)  # Update every 2 seconds

        # Initial update
        self.update_metrics()

    def update_metrics(self):

        # Get system performance metrics
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        disk_free = psutil.disk_usage('/').free / 1024 ** 3

        # Update labels
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage}%, Free: {disk_free:.2f} GB")

        # Get processes info
        processes = self.get_processes_info()
        self.processes_text.setText(processes)

        # Get open files info
        open_files = self.get_open_files_info()
        self.open_files_text.setText(open_files)

    def get_processes_info(self):
        process_list = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                info = proc.info
                process_list.append(
                    f"PID: {info['pid']} | Name: {info['name']}"
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return "\n".join(process_list)

    def get_open_files_info(self):
        open_files_list = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                files = proc.open_files()
                if files:
                    open_files_list.append(f"PID: {proc.info['pid']} | Name: {proc.info['name']} | Open Files:")
                    for file in files:
                        open_files_list.append(f"    {file.path}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return "\n".join(open_files_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
