import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QComboBox
)

class ServiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет ремонта бензоинструмента")
        self.setGeometry(100, 100, 800, 500)
        self.init_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect("service_app.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT,
                device TEXT,
                issue TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Поля ввода
        form_layout = QHBoxLayout()
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("ФИО Клиента")
        self.device_input = QLineEdit()
        self.device_input.setPlaceholderText("Инструмент / Модель")
        self.issue_input = QLineEdit()
        self.issue_input.setPlaceholderText("Неисправность")
        
        form_layout.addWidget(self.client_input)
        form_layout.addWidget(self.device_input)
        form_layout.addWidget(self.issue_input)
        layout.addLayout(form_layout)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Добавить заказ")
        add_btn.clicked.connect(self.add_order)
        delete_btn = QPushButton("Удалить выбранный заказ")
        delete_btn.clicked.connect(self.delete_order)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)

        # Таблица заказов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Клиент", "Инструмент", "Неисправность", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.load_orders()

    def add_order(self):
        client = self.client_input.text().strip()
        device = self.device_input.text().strip()
        issue = self.issue_input.text().strip()

        if not client or not device or not issue:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        self.cursor.execute(
            "INSERT INTO orders (client, device, issue, status) VALUES (?, ?, ?, ?)",
            (client, device, issue, "В работе")
        )
        self.conn.commit()

        self.client_input.clear()
        self.device_input.clear()
        self.issue_input.clear()
        self.load_orders()

    def load_orders(self):
        self.table.setRowCount(0)
        self.cursor.execute("SELECT * FROM orders")
        rows = self.cursor.fetchall()
        for row_idx, row_data in enumerate(rows):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def delete_order(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления!")
            return

        order_id = self.table.item(selected_row, 0).text()
        self.cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.conn.commit()
        self.load_orders()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServiceApp()
    window.show()
    sys.exit(app.exec())
