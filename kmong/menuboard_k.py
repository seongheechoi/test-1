from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_a = QPushButton('a')
        self.button_b = QPushButton('b')
        self.button_c = QPushButton('c')
        self.button_d = QPushButton('d')

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['텍스트', '클릭 수', '버튼'])

        layout = QVBoxLayout()
        layout.addWidget(self.button_a)
        layout.addWidget(self.button_b)
        layout.addWidget(self.button_c)
        layout.addWidget(self.button_d)
        layout.addWidget(self.table_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button_a.clicked.connect(lambda: self.update_table('a'))
        self.button_b.clicked.connect(lambda: self.update_table('b'))
        self.button_c.clicked.connect(lambda: self.update_table('c'))
        self.button_d.clicked.connect(lambda: self.update_table('d'))

        self.click_counts = {}

        self.table_widget.cellClicked.connect(self.activate_button)

    def update_table(self, text):
        if text in self.click_counts:
            self.click_counts[text]+= 1
            for row in range(self.table_widget.rowCount()):
                if self.table_widget.item(row, 0).text() == text:
                    self.table_widget.item(row, 1).setText(str(self.click_counts[text]))
                    break
        else:
            self.click_counts[text]= 1
            row_count = self.table_widget.rowCount()
            self.table_widget.setRowCount(row_count + 1)
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(text))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(self.click_counts[text])))

    def activate_button(self, row, column):
        if column == 2:
            button_item = self.table_widget.item(row, column)
            if button_item is not None:
                button_text = button_item.text()
                if button_text == '0':
                    return

            button = QPushButton('Click')
            button.clicked.connect(lambda: self.decrease_count(row))
            self.table_widget.setCellWidget(row, column, button)

    def decrease_count(self, row):
        count_item = self.table_widget.item(row, 1)
        if count_item is not None:
            count = int(count_item.text())
            if count > 0:
                count -= 1
                count_item.setText(str(count))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
