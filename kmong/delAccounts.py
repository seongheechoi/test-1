import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox

class delAccount(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Account Deletion")
        self.setGeometry(100, 100, 500, 300)

        # 테이블 위젯 생성
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Passwd"])
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        # 삭제 버튼 생성
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_rows)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        self.setStyleSheet("""
                    QDialog {
                        background-color: #f2f2f2;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 20px;
                    }

                    QLabel {
                        font-size: 14pt;
                        font-weight: bold;
                        font-family: "맑은 고딕";
                    }

                    QLineEdit {
                        height: 30px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 16pt;
                        font-family: "맑은 고딕";
                    }

                    QPushButton {
                        height: 60px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16pt;
                        font-family: "맑은 고딕";
                        font-weight: bold;
                    }

                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)

        # 'user.pkl' 파일에서 데이터 읽어오기
        self.load_data()

    def load_data(self):
        try:
            data = pd.read_pickle("user.pkl")
            self.table_widget.setRowCount(len(data))

            for i, row in enumerate(data.iterrows()):
                for j, value in enumerate(row[1]):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(i, j, item)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File 'user.pkl' not found.")

    def delete_selected_rows(self):
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        if len(selected_rows) == 0:
            QMessageBox.warning(self, "Warning", "No rows selected.")
            return

        data = pd.read_pickle("user.pkl")
        data = data.drop(list(selected_rows))
        data = data.reset_index(drop=True)
        data.to_pickle("user.pkl")

        self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = delAccount()
    window.show()
    sys.exit(app.exec_())
