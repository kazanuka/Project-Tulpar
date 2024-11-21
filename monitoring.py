import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Performance Monitor")
        self.setGeometry(100, 100, 400, 300)

        # Main Widget
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # Layout
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Labels for CPU, RAM, Disk Usage
        self.cpu_label = QLabel(self)
        self.ram_label = QLabel(self)
        self.disk_label = QLabel(self)

        # Set font and style for labels
        font = QFont("Arial", 16, QFont.Bold)
        self.cpu_label.setFont(font)
        self.ram_label.setFont(font)
        self.disk_label.setFont(font)

        # Set color palette for labels
        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.cpu_label.setPalette(palette)
        self.ram_label.setPalette(palette)
        self.disk_label.setPalette(palette)

        # Add labels to layout
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)

        # Set background color
        self.setStyleSheet("background-color: #2E3440;")

        # Timer to update the metrics
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)  # Update every second

        # Initial update
        self.update_metrics()

    def update_metrics(self):
        # Get system performance metrics
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Update labels
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
