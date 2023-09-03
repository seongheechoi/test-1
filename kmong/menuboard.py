# 기본 라이브러리 & ML 라이브러리
import sys, os  # sys, os호출 라이브러리
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QWidget, QScrollArea, QSpacerItem, QSizePolicy, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic
import pandas as pd
import numpy as np
from delAccounts import delAccount
from addAccounts import addUsers

# 초기 Setting
form_class=uic.loadUiType('menuboard_test.ui')[0]  # form_class변수에 ui호출

class MyWindow(QMainWindow, form_class):  # MyWindow Class로 생성 후, QMainWindow, UI 상속받기
    def __init__(self):
        super().__init__()
        self.setupUi(self) # UI를 통해 윈도우화면 자동 생성
        self.setWindowTitle("DIC - Project 8조")  # 윈도우 이름 설정
        self.user = None
        self.isAdmin = 'No'
        self.del_widget = None
        self.create_widget = None
        self.actionCreat_Account.triggered.connect(self.createAccount)
        self.actionDelete_Account.triggered.connect(self.deleteAccount)
        self.L1_table_btn.clicked.connect(self.L1_table_btnq)  # table_완료btn 함수지정
        self.L1_table.cellClicked.connect(self.L1_table_editq)
        # self.df_menu = pd.DataFrame(index=range(0, 27),
        #                             columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴확인 df(한국어)
        # self.df_cnt_db = np.zeros((28, 5))
        # self.df_cnt = pd.DataFrame(self.df_cnt_db, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
        # self.df_position = pd.DataFrame(index=range(0, 100), columns=['menu_row', 'menu_col'])  # 메뉴확인 df와 table 위치확인
        self.click_counts = {}
        ####################################################################
        # 언어변경
        self.comboBox.currentTextChanged.connect(self.comboBoxTextChanged)
        #####################################################################

        with open("style_tab.qss", "r") as f:
            style_sheet = f.read()
        with open("style_tab2.qss", "r") as f:
            style_sheet2 = f.read()
        with open("style_btn1.qss", "r") as f:
            self.style_sheet_btn = f.read()
        # self.tabWidget_1.setStyleSheet(style_sheet)
        # self.tabWidget_2.setStyleSheet(style_sheet2)
        #####################################################################3

        ###################################################################################
        # 메뉴류 탭 세팅 -
        # 새우류(Shrimp)
        self.tabWidget_2.setTabText(0, "새우류\n(Shrimp)")
        self.tabWidget_2.setTabText(1, "오징어류\n(Squid)")
        self.tabWidget_2.setTabText(2, "생선류\n(Fish)")
        self.tabWidget_2.setTabText(3, "고기류\n(Meat)")
        self.tabWidget_2.setTabText(4, "기타류\n(Other)")
        ####################################################################################
        ####################################################################################
        # 버튼생성
        self.btn_layout0 = QVBoxLayout()
        self.gridlayout0 = QtWidgets.QGridLayout()
        self.btn_layout1 = QVBoxLayout()
        self.gridlayout1 = QtWidgets.QGridLayout()
        self.btn_layout2 = QVBoxLayout()
        self.gridlayout2 = QtWidgets.QGridLayout()
        self.btn_layout3 = QVBoxLayout()
        self.gridlayout3 = QtWidgets.QGridLayout()
        self.btn_layout4 = QVBoxLayout()
        self.gridlayout4 = QtWidgets.QGridLayout()
        self.makeBtns('Korea')

        self.scroll_area0 = QScrollArea()
        self.scroll_area0.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 수직 스크롤 바 항상 표시
        self.scroll_area0.setWidgetResizable(True)
        self.scroll_widget0 = QWidget()  # 스크롤 위젯 생성
        self.scroll_widget0.setLayout(self.gridlayout0)
        self.scroll_area0.setWidget(self.scroll_widget0)
        self.btn_layout0.addWidget(self.scroll_area0)
        self.tab_shrimp.setLayout(self.btn_layout0)

        self.scroll_area1 = QScrollArea()
        self.scroll_area1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 수직 스크롤 바 항상 표시
        self.scroll_area1.setWidgetResizable(True)
        self.scroll_widget1 = QWidget()  # 스크롤 위젯 생성
        self.scroll_widget1.setLayout(self.gridlayout1)
        self.scroll_area1.setWidget(self.scroll_widget1)
        self.btn_layout1.addWidget(self.scroll_area1)
        self.tab_squid.setLayout(self.btn_layout1)

        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 수직 스크롤 바 항상 표시
        self.scroll_area2.setWidgetResizable(True)
        self.scroll_widget2 = QWidget()  # 스크롤 위젯 생성
        self.scroll_widget2.setLayout(self.gridlayout2)
        self.scroll_area2.setWidget(self.scroll_widget2)
        self.btn_layout2.addWidget(self.scroll_area2)
        self.tab_fish.setLayout(self.btn_layout2)

        self.scroll_area3 = QScrollArea()
        self.scroll_area3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 수직 스크롤 바 항상 표시
        self.scroll_area3.setWidgetResizable(True)
        self.scroll_widget3 = QWidget()  # 스크롤 위젯 생성
        self.scroll_widget3.setLayout(self.gridlayout3)
        self.scroll_area3.setWidget(self.scroll_widget3)
        self.btn_layout3.addWidget(self.scroll_area3)
        self.tab_meat.setLayout(self.btn_layout3)

        self.scroll_area4 = QScrollArea()
        self.scroll_area4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 수직 스크롤 바 항상 표시
        self.scroll_area4.setWidgetResizable(True)
        self.scroll_widget4 = QWidget()  # 스크롤 위젯 생성
        self.scroll_widget4.setLayout(self.gridlayout4)
        self.scroll_area4.setWidget(self.scroll_widget4)
        self.btn_layout4.addWidget(self.scroll_area4)
        self.tab_other.setLayout(self.btn_layout4)

        ###################################################################################


    def set_user(self, user):
        self.user = user
        if self.user == 'admin':
            self.isAdmin = 'yes'

    def set_password(self, password):
        self.password = password

    def createAccount(self):
        if (self.isAdmin == 'yes'):
            self.create_widget = addUsers()
            self.create_widget.show()
        else:
            QMessageBox.warning(self, "id 에러", "접근권한이 없습니다.")

    def deleteAccount(self):
        if (self.isAdmin == 'yes'):
            self.del_widget = delAccount()
            self.del_widget.show()
        else:
            QMessageBox.warning(self, "id 에러", "접근권한이 없습니다.")

    def makeBtns(self, text):
        self.clearButtons()
        # 버튼 생성 및 배치
        df0 = pd.read_csv('List_shrimp.csv')
        df1 = pd.read_csv('List_squid.csv')
        df2 = pd.read_csv('List_fish.csv')
        df3 = pd.read_csv('List_meat.csv')
        df4 = pd.read_csv('List_other.csv')

        for i, row0 in df0.iterrows():
            button = QPushButton(row0[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row0[text]: self.buttonClicked(btn))
            row0 = i // 4
            col0 = i % 4
            self.gridlayout0.addWidget(button, row0, col0)
        spacer0 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout0.addItem(spacer0, row0 + 1, 0, 1, 4)

        for i, row1 in df1.iterrows():
            button = QPushButton(row1[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row1[text]: self.buttonClicked(btn))
            row1 = i // 4
            col1 = i % 4
            self.gridlayout1.addWidget(button, row1, col1)
        spacer1 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout1.addItem(spacer1, row1 + 1, 0, 1, 4)

        for i, row2 in df2.iterrows():
            button = QPushButton(row2[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row2[text]: self.buttonClicked(btn))
            row2 = i // 4
            col2 = i % 4
            self.gridlayout2.addWidget(button, row2, col2)
        spacer2 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout2.addItem(spacer2, row2 + 1, 0, 1, 4)

        for i, row3 in df3.iterrows():
            button = QPushButton(row3[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row3[text]: self.buttonClicked(btn))
            row3 = i // 4
            col3 = i % 4
            self.gridlayout3.addWidget(button, row3, col3)
        spacer3 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout3.addItem(spacer3, row3 + 1, 0, 1, 4)

        for i, row4 in df4.iterrows():
            button = QPushButton(row4[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row4[text]: self.buttonClicked(btn))
            row4 = i // 4
            col4 = i % 4
            self.gridlayout4.addWidget(button, row4, col4)
        spacer4 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout4.addItem(spacer4, row4 + 1, 0, 1, 4)

    def clearButtons(self):
        while self.gridlayout0.count():
            item = self.gridlayout0.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.gridlayout1.count():
            item = self.gridlayout1.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.gridlayout2.count():
            item = self.gridlayout2.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.gridlayout3.count():
            item = self.gridlayout3.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        while self.gridlayout4.count():
            item = self.gridlayout4.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def buttonClicked(self, menu):
        idx = self.tabWidget_2.currentIndex()
        self.L1_tableq(idx, menu)

    def comboBoxTextChanged(self, text):
        if text == '한국어':
            self.makeBtns('Korea')
        elif text == '영어':
            self.makeBtns('English')
        elif text == '태국':
            self.makeBtns('Thailand')
        else:
            self.makeBtns('Vietnam')



    def L1_tableq(self, tab, text): # table 상태창
        if text in self.click_counts:
            self.click_counts[text] += 1
            for row in range(self.L1_table.rowCount()):
                if self.L1_table.item(row, 0).text() == text:
                    print(self.L1_table.item(row, 0).text())
                    self.L1_table.item(row, 1).setText(str(self.click_counts[text]))
                    break
        else:
            self.click_counts[text] = 1
            row_count = self.L1_table.rowCount()
            self.L1_table.setRowCount(row_count + 1)
            self.L1_table.setItem(row_count, 0, QTableWidgetItem(text))
            self.L1_table.setItem(row_count, 1, QTableWidgetItem(str(self.click_counts[text])))

    def L1_table_editq(self):
        selected_box = self.L1_table.selectedIndexes()  # 선택된 좌표값 받아오기
        # print(selected_box[0].row())  #int
        # print(selected_box[0].column())  #int

        if selected_box[0].column() == 2:  # 수량 +
            add_df_row = self.df_position.iat[selected_box[0].row(), 0]
            add_df_col = self.df_position.iat[selected_box[0].row(), 1]
            self.df_cnt.iat[add_df_col, add_df_row] += 1
            self.L1_table.setItem(selected_box[0].row(), 1, QTableWidgetItem(
                str(int(self.df_cnt.iat[add_df_col, add_df_row]))))  # table에 cnt update

        if selected_box[0].column() == 3:  # 수량 -
            sub_df_row = self.df_position.iat[selected_box[0].row(), 0]
            sub_df_col = self.df_position.iat[selected_box[0].row(), 1]
            if self.df_cnt.iat[sub_df_col, sub_df_row] == 1:
                pass
            else:
                self.df_cnt.iat[sub_df_col, sub_df_row] -= 1
                self.L1_table.setItem(selected_box[0].row(), 1, QTableWidgetItem(
                    str(int(self.df_cnt.iat[sub_df_col, sub_df_row]))))  # table에 cnt update

        if selected_box[0].column() == 4:
            RowLeft = self.L1_table.rowCount()  # 현재 행 수 확인
            if RowLeft == 1:
                del_df_row = self.df_position.iat[selected_box[0].row(), 0]
                del_df_col = self.df_position.iat[selected_box[0].row(), 1]
                self.df_cnt.iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제
                for col in range(5):
                    self.L1_table.setItem(0, col, None)  # 빈칸표시
            else:
                self.L1_table.removeRow(selected_box[0].row())  # 선택된 행 삭제
                del_df_row = self.df_position.iat[selected_box[0].row(), 0]
                del_df_col = self.df_position.iat[selected_box[0].row(), 1]
                self.df_cnt.iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제

    def L1_table_btnq(self):  # 완료처리
        if self.L1_table.item(0, 0) == None:
            pass
        else:
            data_dict = {}
            for row in range(self.L1_table.rowCount()):
                menu_item = self.L1_table.item(row, 0).text()
                menu_cnt = self.L1_table.item(row, 1).text()
                data_dict[menu_item] = menu_cnt
            text = ""
            for name, cnt in data_dict.items():
                text += f"{name}:{cnt},  "
            self.L2_text.setPlainText(text)

            self.df_cnt = pd.DataFrame(np.zeros((28, 5)), columns=['shrimp', 'squid', 'fish', 'other', 'meat']) # df_cnt 초기화
            self.df_position = pd.DataFrame(index=range(0, 100),columns=['menu_row', 'menu_col'])  # 메뉴확인 df와 table 위치확인
            self.L1_table.setRowCount(1)  # row 삭제
            self.L1_table.setColumnCount(3)  #column 3개
            self.L1_table.setHorizontalHeaderLabels(['주문메뉴','수량','+', '-', '삭제'])  # column 입력
            self.L1_table.setColumnWidth(0, int((self.L1_table.width() - 20) * 6.5 / 10))  # 메뉴
            self.L1_table.setColumnWidth(1, int((self.L1_table.width() - 20) * 1 / 10))  # 수량
            self.L1_table.setColumnWidth(2, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량추가
            self.L1_table.setColumnWidth(3, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량감소
            self.L1_table.setColumnWidth(4, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량삭제
            for col in range(5):
                self.L1_table.setItem(0, col, None) #빈칸표시

if __name__=="__main__":  # 프로그램 실행
    app = QApplication(sys.argv)
    myWindow=MyWindow()   # MyWindow 함수 변수화
    from PyQt5.QtGui import QFont
    font = QFont('./fonts/KoHo/KoHo-Bold.ttf')
    myWindow.setFont(font)
    myWindow.show()  # Window 화면 실행
    app.exec_()  # 이벤트 loop 실행

