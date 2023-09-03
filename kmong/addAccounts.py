import pickle
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout


class addUsers(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Registration")
        self.layout = QVBoxLayout()

        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_input)

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_user)
        self.layout.addWidget(self.create_button)

        self.setLayout(self.layout)

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

    def create_user(self):
        user_id = self.id_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            with open("user.pkl", "rb") as file:
                users = pickle.load(file)
        except FileNotFoundError:
            users = pd.DataFrame(columns=["id", "passwd"])

        if user_id in users["id"].values:
            QMessageBox.warning(self, "Error", "User ID already exists.")
        else:
            new_user = pd.DataFrame({"id": [user_id], "passwd": [password]})
            users = pd.concat([users, new_user], ignore_index=True)
            with open("user.pkl", "wb") as file:
                pickle.dump(users, file)
            QMessageBox.information(self, "Success", "New account created.")

        self.id_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()


if __name__ == "__main__":
    app = QApplication([])
    widget = addUsers()
    widget.show()
    app.exec_()
