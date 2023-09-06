import sys, os, datetime
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QWidget, QScrollArea, QSpacerItem, QSizePolicy, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic
import pandas as pd
import numpy as np
from delAccounts import delAccount
from addAccounts import addUsers
from PyQt5.QtGui import QFont

font_koho_bold = QFont('KoHo-Bold.ttf')
font = QFont('Koho Bold')

# 초기 Setting
form_class=uic.loadUiType('menuboard_test_lkk.ui')[0]  # form_class변수에 ui호출

class MyWindow(QMainWindow, form_class):  # MyWindow Class로 생성 후, QMainWindow, UI 상속받기
    def __init__(self):
        super().__init__()
        self.setupUi(self) # UI를 통해 윈도우화면 자동 생성
        self.setWindowTitle("DaeSung")  # 윈도우 이름 설정
        self.user = None
        self.isAdmin = 'No'
        self.del_widget = None
        self.create_widget = None
        self.actionCreat_Account.triggered.connect(self.createAccount)
        self.actionDelete_Account.triggered.connect(self.deleteAccount)
        self.L1_table_btn.clicked.connect(self.L1_table_btnq)  # table_완료btn 함수지정
        self.L1_table.cellClicked.connect(self.L1_table_editq)
        self.L2_btn.clicked.connect(self.L2_btnq)  # history 저장
        try:  # history불러오기
            order_history = pd.read_csv('Order_History.csv', encoding='cp949', index_col=0)
            order_history = order_history.reset_index(drop=True)
            self.L2_table.setRowCount(len(order_history))
            for i, row_data in order_history.iterrows():
                for j, val in enumerate(row_data):
                    item = QTableWidgetItem(str(val))
                    self.L2_table.setItem(i, j, item)
        except FileNotFoundError:
            print(f'파일을 찾을 수 없습니다')
        except Exception as e:
            print(f'오류 발생: {e}')
        self.L1_table.setColumnWidth(0, int((self.L1_table.width() - 20) * 2.5 / 10))  # 메뉴
        self.L1_table.setColumnWidth(1, int((self.L1_table.width() - 20) * 3.5 / 10))  # 메뉴
        self.L1_table.setColumnWidth(2, int((self.L1_table.width() - 20) * 1 / 10))  # 수량
        self.L1_table.setColumnWidth(3, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량추가
        self.L1_table.setColumnWidth(4, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량감소
        self.L1_table.setColumnWidth(5, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량삭제
        self.L2_table.setColumnWidth(0, int((self.L2_table.width() - 20) * 2 / 10))
        self.L2_table.setColumnWidth(1, int((self.L2_table.width() - 20) * 1 / 10))
        self.L2_table.setColumnWidth(2, int((self.L2_table.width() - 20) * 6 / 10))
        ####################################################################
        # 변수정의 DB :  python에서는 변수를 동적으로 생성하는 것이 권장되지 않기에, 리스트를 통한 DataFrame 구조로 설정하려고 함
        # DataFrame: (5 * 50)으로 설정 (Tab Max개수 5개, Menu Max개수는 50개) (UI 구조와 연동을 위해 최대값으로 설정하여 정리함)
        self.click_counts = {}
        self.df_menu = []
        for i in range(4):
            df0 = pd.read_csv('List_shrimp.csv', index_col=0).iloc[:,i]
            df1 = pd.read_csv('List_squid.csv', index_col=0).iloc[:,i]
            df2 = pd.read_csv('List_fish.csv', index_col=0).iloc[:,i]
            df3 = pd.read_csv('List_meat.csv', index_col=0).iloc[:,i]
            df4 = pd.read_csv('List_other.csv', index_col=0).iloc[:,i]
            dft = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
            self.df_menu.append(dft)

        self.df_cnt = []
        self.df_cnt_db = np.zeros((len(self.df_menu[0]), 5))
        for i in range(4):
            self.df_cnt.append(pd.DataFrame(self.df_cnt_db, columns=['shrimp', 'squid', 'fish', 'meat', 'other']))  # 메뉴수량 df

        self.initial_cnt = self.df_cnt.copy()

        self.df_position = []
        for i in range(4):
            self.df_position.append(pd.DataFrame(index=range(0, 100), columns=['menu_row', 'menu_col']))# 메뉴확인 df와 table 위치확인

        self.df_posInitial = self.df_position.copy()

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
        # 메뉴류 탭 세팅 - 한글/영어 사용이 gui문제가 잇어 영어만 사용함

        self.tabWidget_2.setTabText(0, "Shrimp")#새우류\n(Shrimp)")
        self.tabWidget_2.setTabText(1, "Squid")#오징어류\n(Squid)")
        self.tabWidget_2.setTabText(2, "Fish")#생선류\n(Fish)")
        self.tabWidget_2.setTabText(3, "Meat")#고기류\n(Meat)")
        self.tabWidget_2.setTabText(4, "Other")#기타류\n(Other)")

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
            button.clicked.connect(lambda checked, btn=row0[text], idx=i: self.buttonClicked(btn, idx))
            row0 = i // 4
            col0 = i % 4
            self.gridlayout0.addWidget(button, row0, col0)
        spacer0 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout0.addItem(spacer0, row0 + 1, 0, 1, 4)

        for i, row1 in df1.iterrows():
            button = QPushButton(row1[text])

            button.setStyleSheet(self.style_sheet_btn)
            button.setFont(font)
            button.clicked.connect(lambda checked, btn=row1[text], idx=i: self.buttonClicked(btn, idx))
            row1 = i // 4
            col1 = i % 4
            self.gridlayout1.addWidget(button, row1, col1)
        spacer1 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout1.addItem(spacer1, row1 + 1, 0, 1, 4)

        for i, row2 in df2.iterrows():
            button = QPushButton(row2[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row2[text], idx=i: self.buttonClicked(btn, idx))
            row2 = i // 4
            col2 = i % 4
            self.gridlayout2.addWidget(button, row2, col2)
        spacer2 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout2.addItem(spacer2, row2 + 1, 0, 1, 4)

        for i, row3 in df3.iterrows():
            button = QPushButton(row3[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row3[text], idx=i: self.buttonClicked(btn, idx))
            row3 = i // 4
            col3 = i % 4
            self.gridlayout3.addWidget(button, row3, col3)
        spacer3 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
        self.gridlayout3.addItem(spacer3, row3 + 1, 0, 1, 4)

        for i, row4 in df4.iterrows():
            button = QPushButton(row4[text])
            button.setStyleSheet(self.style_sheet_btn)
            button.clicked.connect(lambda checked, btn=row4[text], idx=i: self.buttonClicked(btn, idx))
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

    def buttonClicked(self, menu, menu_i):
        idx = self.tabWidget_2.currentIndex()
        idx_name=self.tabWidget_2.tabText(idx)
        self.L1_tableq(idx, idx_name, menu, menu_i)

    def comboBoxTextChanged(self, text):
        if text == '한국어':
            self.makeBtns('Korea')
        elif text == '영어':
            self.makeBtns('English')
        elif text == '태국':
            self.makeBtns('Thailand')
        else:
            self.makeBtns('Vietnam')

    ## 기존 코드 최적화 - ChatGPT
    def L1_tableq(self, tab, tab_name, menu, menu_i):  # table 상태창
        self.current_index = 0
        self.df_cnt[self.current_index].iat[menu_i, tab] += 1  # menu 수량 추가
        self.currentRowCount = self.L1_table.rowCount()  # 현재 행 수 확인

        # table에 선택된 메뉴 존재여부 확인
        for i in range(self.currentRowCount):
            if self.L1_table.item(i, 0) is not None:
                if str(tab_name) == self.L1_table.item(i, 0).text() and self.df_menu[self.current_index].iat[
                    menu_i, tab] == self.L1_table.item(i, 1).text():
                    cnt = int(self.L1_table.item(i, 2).text()) + 1  # 현재 cnt 값 가져오기
                    self.L1_table.setItem(i, 2, QTableWidgetItem(str(cnt)))  # table에 cnt update
                    self.df_position[self.current_index].iat[i, 0] = tab
                    self.df_position[self.current_index].iat[i, 1] = menu_i
                    return

        if self.L1_table.item(0, 0) is None:
            row = 0
        else:
            row = self.currentRowCount

        ## 수량만 클릭해서 수정이 가능하고 나머지는 수정 비활성화
        item0 = QTableWidgetItem(str(tab_name))
        item0.setFlags(item0.flags() & ~Qt.ItemIsEditable)
        item1 = QTableWidgetItem(str(self.df_menu[self.current_index].iat[menu_i, tab]))
        item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
        item3 = QTableWidgetItem('+')
        item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
        item4 = QTableWidgetItem('-')
        item4.setFlags(item4.flags() & ~Qt.ItemIsEditable)
        item5 = QTableWidgetItem('del')
        item5.setFlags(item5.flags() & ~Qt.ItemIsEditable)

        self.L1_table.insertRow(row)  # 행 추가
        self.L1_table.setItem(row, 0, item0)  # table에 내용 update
        self.L1_table.setItem(row, 1, item1)
        self.L1_table.setItem(row, 2, QTableWidgetItem(str(int(self.df_cnt[self.current_index].iat[menu_i, tab]))))
        self.L1_table.setItem(row, 3, item3)
        self.L1_table.setItem(row, 4, item4)
        self.L1_table.setItem(row, 5, item5)

        self.df_position[self.current_index].iat[row, 0] = tab
        self.df_position[self.current_index].iat[row, 1] = menu_i

    def L1_table_editq(self):
        selected_box = self.L1_table.selectedIndexes()  # 선택된 좌표값 받아오기
        # print(selected_box[0].row())  #int
        # print(selected_box[0].column())  #int

        if selected_box[0].column() == 3:  # 수량 +
            add_df_row = self.df_position[self.current_index].iat[selected_box[0].row(), 0]
            add_df_col = self.df_position[self.current_index].iat[selected_box[0].row(), 1]
            self.df_cnt[self.current_index].iat[add_df_col, add_df_row] += 1
            self.L1_table.setItem(selected_box[0].row(), 2, QTableWidgetItem(str(int(self.df_cnt[self.current_index].iat[add_df_col, add_df_row]))))  # table에 cnt update

        if selected_box[0].column() == 4:  # 수량 -
            sub_df_row = self.df_position[self.current_index].iat[selected_box[0].row(), 0]
            sub_df_col = self.df_position[self.current_index].iat[selected_box[0].row(), 1]
            if self.df_cnt[self.current_index].iat[sub_df_col, sub_df_row] == 1:
                pass
            else:
                self.df_cnt[self.current_index].iat[sub_df_col, sub_df_row] -= 1
                self.L1_table.setItem(selected_box[0].row(), 2, QTableWidgetItem(str(int(self.df_cnt[self.current_index].iat[sub_df_col, sub_df_row]))))  # table에 cnt update

        if selected_box[0].column() == 5:
            RowLeft = self.L1_table.rowCount()  # 현재 행 수 확인
            # if RowLeft == 1:
            #     del_df_row = self.df_position.iat[selected_box[0].row(), 0]
            #     del_df_col = self.df_position.iat[selected_box[0].row(), 1]
            #     self.df_cnt.iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제
            #     for col in range(5):
            #         self.L1_table.setItem(0, col, None)  # 빈칸표시
            # else:
            #     self.L1_table.removeRow(selected_box[0].row())  # 선택된 행 삭제
            #     del_df_row = self.df_position.iat[selected_box[0].row(), 0]
            #     del_df_col = self.df_position.iat[selected_box[0].row(), 1]
            #     self.df_cnt.iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제
            # if RowLeft == 1:
            #     self.df_cnt = pd.DataFrame(np.zeros((28, 5)),columns=['shrimp', 'squid', 'fish', 'other', 'meat'])  # df_cnt 초기화
            #     # for col in range(5):
            #     #     self.L1_table.setItem(0, col, None)  # 빈칸표시
            # else:

            # 1번행이 필요없기 때문에 RowLeft 필요없음
            self.L1_table.removeRow(selected_box[0].row()) # 선택된 행 삭제
            del_df_row=self.df_position[self.current_index].iat[selected_box[0].row(), 0]
            del_df_col=self.df_position[self.current_index].iat[selected_box[0].row(), 1]
            self.df_cnt[self.current_index].iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제
            self.df_position[self.current_index].drop(selected_box[0].row(), axis=0, inplace=True)
            self.df_position[self.current_index].loc['100']= [np.nan,np.nan]
            self.df_position[self.current_index].reset_index(inplace=True,drop=True)


        # print(self.df_menu.head(3))
        # print(self.df_menu.tail(3))
        # print(1)
        # print(self.df_cnt.head(3))
        # print(self.df_cnt.tail(3))
        # print(2)
        # print(self.df_position.head(3))
        # print(self.df_position.tail(3))
        # print(3)

    def L1_table_btnq(self):  # 완료처리
        data_dict = {}
        for row in range(self.L1_table.rowCount()):
            menu_category = self.L1_table.item(row, 0).text()
            menu_item = self.L1_table.item(row, 1).text()
            menu_cnt = self.L1_table.item(row, 2).text()
            data_dict[menu_item] = menu_cnt

        data_df = pd.DataFrame.from_dict(data_dict, orient='index', columns=['menu_cnt'])
        data_df.reset_index(inplace=True)
        data_df.columns = ['menu_item', 'menu_cnt']
        data_df['menu_category'] = self.L1_table.item(0, 0).text()

        items = [f"{row['menu_category']}_{row['menu_item']}: {row['menu_cnt']},  " for _, row in data_df.iterrows()]
        combined_items = ''.join(items)
        self.L2_text.setPlainText(combined_items)

        self.df_cnt = self.initial_cnt
        self.df_position = self.df_posInitial  # 메뉴확인 df와 table 위치확인
        self.L1_table.setRowCount(0)  # row 삭제
        self.L1_table.setColumnCount(6)  # column 6개
        self.L1_table.setHorizontalHeaderLabels(['카테고리', '주문메뉴', '수량', '+', '-', '삭제'])  # column 입력
        self.L1_table.setColumnWidth(0, int((self.L1_table.width() - 20) * 2.5 / 10))  # 메뉴
        self.L1_table.setColumnWidth(1, int((self.L1_table.width() - 20) * 3.5 / 10))  # 메뉴
        self.L1_table.setColumnWidth(2, int((self.L1_table.width() - 20) * 1 / 10))  # 수량
        self.L1_table.setColumnWidth(3, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량추가
        self.L1_table.setColumnWidth(4, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량감소
        self.L1_table.setColumnWidth(5, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량삭제

    def L2_btnq(self):  # History저장
        if self.user == None:
            director='director'
        else:
            director=self.user

        if self.L2_text.toPlainText() == '':
            pass
        else:
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d  %H:%M:%S")
            if self.L2_table.item(0, 0) == None:
                self.L2_table.setItem(0, 0, QTableWidgetItem(str(formatted_date)))  # table에 내용 update
                self.L2_table.setItem(0, 1, QTableWidgetItem(str(director)))  # table에 내용 update
                self.L2_table.setItem(0, 2, QTableWidgetItem(str(self.L2_text.toPlainText())))  # table에 cnt update
            else:
                self.L2_table.insertRow(self.currentRowCount)  # 행 추가
                self.L2_table.setItem(self.currentRowCount, 0,QTableWidgetItem(str(formatted_date)))  # table에 내용 update
                self.L2_table.setItem(self.currentRowCount, 1,QTableWidgetItem(str(director)))  # table에 내용 update
                self.L2_table.setItem(self.currentRowCount, 2,QTableWidgetItem(str(self.L2_text.toPlainText())))  # table에 cnt update

            order_data = []
            for row in range(self.L2_table.rowCount()):
                row_data = []
                for col in range(self.L2_table.columnCount()):
                    item = self.L2_table.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                order_data.append(row_data)

            # 추출한 데이터를 Pandas DataFrame으로 변환
            order_data_df = pd.DataFrame(order_data, columns=['time', 'Director', 'Order History'])
            with open(os.getcwd() + '\Order_History.csv', 'a', newline="", encoding='cp949') as csvfile:
                order_data_df.to_csv(csvfile, header=csvfile.tell() == 0)  # 존재하지 않는 경우, 파일 생성, 있으면 내용 추가

if __name__=="__main__":  # 프로그램 실행
    app = QApplication(sys.argv)
    myWindow=MyWindow()   # MyWindow 함수 변수화
    myWindow.show()  # Window 화면 실행
    app.exec_()  # 이벤트 loop 실행