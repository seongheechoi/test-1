import sys, os  # sys, os호출 라이브러리
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd

from PyQt5 import uic  # PyQt5 내 uic호출
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView)  # PyQt5 내 위젯 호출
                            #어플 실행,   윈도우창 실행,  파일불러오기,  메세지박스,  테이블 위젯
from PyQt5.QtGui import QFont

font = QFont('./fonts/KoHo/KoHo-Bold.ttf')
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")

        self.username_label = QLabel("아이디:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("비밀번호:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("로그인")
        self.login_button.clicked.connect(self.login)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # 스타일 적용
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
    def get_user(self):
        return self.username_input.text()

    def get_password(self):
        return self.password_input.text()

    def login(self):
        id = self.username_input.text()
        password = self.password_input.text()

        if (id == 'admin') and (password == 'admin'):
            self.accept()
        else:
            user_df = pd.read_pickle('user.pkl')
            matching_user_rows = user_df[user_df['id'] == id]

            if not matching_user_rows.empty:
                if (matching_user_rows['passwd'] == password).any():
                    self.accept()
                    return
            QMessageBox.warning(self, "잘못 입력 하셨습니다", "ID와 Password를 다시 확인해주세요.")

if __name__=="__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    login.setFont(font)
    if login.exec_() == QDialog.Accepted:
        from menuboard import MyWindow
        myWindow=MyWindow()
        myWindow.set_user(login.get_user())
        myWindow.set_password(login.get_password())
        myWindow.show()
        app.exec_()