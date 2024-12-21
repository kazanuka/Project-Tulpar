import sys # Sistem kütüphanesi
import psutil # Sistem bilgilerini aldığımız kütüphane
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar, QLineEdit, \
    QTableWidget, QTableWidgetItem, QTabWidget # PyQt5 ek kütüphneleri
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import pyqtgraph as pg


class SystemMonitor(QMainWindow):
    def __init__(self):  #Constructor fonksiyonu
        super().__init__()
        self.setWindowTitle("Sistem Monitörü")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.system_info_tab, self.graphs_tab = QWidget(), QWidget()
        self.tabs.addTab(self.system_info_tab, "Sistem Bilgisi")
        self.tabs.addTab(self.graphs_tab, "Grafikler")

        self.setup_system_info_tab()
        self.setup_graphs_tab()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(3000)
        self.update_metrics()

    def setup_system_info_tab(self): # Sistem bilgilerini bu sekmede gösteriyorum
        layout = QVBoxLayout(self.system_info_tab)
        self.setStyleSheet("background-color: #2e3b4e; color: #ffffff;")
        font = QFont("Arial", 12)
        self.setFont(font)

        self.cpu_label, self.cpu_bar = QLabel("CPU Kullanımı:"), QProgressBar(self)
        self.ram_label, self.ram_bar = QLabel("RAM Kullanımı:"), QProgressBar(self)
        self.disk_label, self.disk_bar = QLabel("Disk Kullanımı:"), QProgressBar(self)

        for bar in [self.cpu_bar, self.ram_bar, self.disk_bar]:
            self.customize_progress_bar(bar)

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_bar)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Process ara...")
        self.search_bar.textChanged.connect(self.search_process)

        self.process_table = QTableWidget(self)
        self.process_table.setColumnCount(2)
        self.process_table.setHorizontalHeaderLabels(["PID", "Process İsmi"])
        self.process_table.setStyleSheet(
            "QTableWidget { background-color: #3c4f65; color: white; gridline-color: #2e3b4e; }"
            "QHeaderView::section { background-color: #3c4f65; color: white; }"
            "QTableWidget::item { padding: 5px; }"
        )
        layout.addWidget(self.search_bar)
        layout.addWidget(self.process_table)

    def setup_graphs_tab(self):# Grafiklerin oluşturulması
        layout = QVBoxLayout(self.graphs_tab)

        self.cpu_graph, self.ram_graph, self.disk_graph = pg.PlotWidget(title="CPU Kullanımı"), pg.PlotWidget(
            title="RAM Kullanımı"), pg.PlotWidget(title="Disk Kullanımı")

        for graph in [self.cpu_graph, self.ram_graph, self.disk_graph]:
            graph.setBackground("#2e3b4e")
            graph.setLabel('left', 'Kullanım (%)')
            graph.setLabel('bottom', 'Zaman')

        layout.addWidget(self.cpu_graph)
        layout.addWidget(self.ram_graph)
        layout.addWidget(self.disk_graph)

        self.cpu_data, self.ram_data, self.disk_data, self.x_data = [], [], [], []

    def customize_progress_bar(self, progress_bar):#Progress bar özellikleri
        progress_bar.setStyleSheet(
            """QProgressBar { border: 1px solid #3c4f65; border-radius: 5px; text-align: center; background-color: #3c4f65; }
               QProgressBar::chunk { background-color: #5cb85c; width: 20px; }"""
        )
        progress_bar.setTextVisible(True)
        progress_bar.setFixedHeight(25)

    def update_metrics(self):#Asıl işlemlerin yapıldığı fonksiyon
        cpu_usages = psutil.cpu_percent(interval=1, percpu=True)
        cpu_usage_avg = sum(cpu_usages) / len(cpu_usages)
        self.cpu_bar.setValue(int(cpu_usage_avg))
        self.cpu_label.setText(f"CPU Kullanımı: {cpu_usage_avg:.1f}%")

        ram_usage = psutil.virtual_memory().percent
        ram_free = psutil.virtual_memory().free /1024 ** 3
        ram_using = psutil.virtual_memory().used /1024 ** 3
        ram_total = psutil.virtual_memory().total / 1024 ** 3


        self.ram_bar.setValue(int(ram_usage))
        self.ram_label.setText(f"RAM Kullanımı: {ram_usage:.1f}%, {ram_free:.1f} GB Boş, {ram_using:.1f} GB Kullanılıyor")

        disk_usage = psutil.disk_usage('/').percent
        disk_free = psutil.disk_usage('/').free / 1024 ** 3
        disk_using = psutil.disk_usage('/').used / 1024 ** 3
        self.disk_bar.setValue(int(disk_usage))
        self.disk_label.setText(f"Disk Kullanımı: {disk_usage:.1f}%, {disk_free:.1f} GB Boş, {disk_using:.1f} GB Kullanılıyor")

        self.process_table.setRowCount(0)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                row = self.process_table.rowCount()
                self.process_table.insertRow(row)
                self.process_table.setItem(row, 0, QTableWidgetItem(str(pid)))
                self.process_table.setItem(row, 1, QTableWidgetItem(name))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.x_data.append(len(self.x_data))
        self.cpu_data.append(cpu_usage_avg)
        self.ram_data.append(ram_usage)
        self.disk_data.append(disk_usage)

        self.cpu_graph.plot(self.x_data, self.cpu_data, pen=pg.mkPen('y'), clear=True)
        self.ram_graph.plot(self.x_data, self.ram_data, pen=pg.mkPen('c'), clear=True)
        self.disk_graph.plot(self.x_data, self.disk_data, pen=pg.mkPen('m'), clear=True)

    def search_process(self): # Process arama
        search_text = self.search_bar.text().lower()
        for row in range(self.process_table.rowCount()):
            process_name = self.process_table.item(row, 1).text().lower()
            if search_text in process_name:
                self.process_table.selectRow(row)
                return
        self.process_table.clearSelection()  


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec_())
