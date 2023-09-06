import sys, os, datetime
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QWidget, QScrollArea, QSpacerItem, QSizePolicy, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import QtWidgets, uic
import pandas as pd
import numpy as np
from delAccounts import delAccount
from addAccounts import addUsers

# 초기 Setting
form_class=uic.loadUiType('menuboard_update.ui')[0]  # form_class변수에 ui호출

class MyWindow(QMainWindow, form_class):  # MyWindow Class로 생성 후, QMainWindow, UI 상속받기
    def __init__(self):
        super().__init__()
        self.setupUi(self) # UI를 통해 윈도우화면 자동 생성
        self.setWindowTitle("DaeSung")  # 윈도우 이름 설정
        self.user = None
        self.isAdmin = 'No'
        self.del_widget = None
        self.create_widget = None
        self.lang_idx = 0
        self.cFonts = []
        id = QFontDatabase.addApplicationFont("./fonts/malgunbd.ttf")
        font = QFontDatabase.applicationFontFamilies(id)
        self.cFonts.append(font[0])
        id = QFontDatabase.addApplicationFont("./fonts/tahomabd.ttf")
        font = QFontDatabase.applicationFontFamilies(id)
        self.cFonts.append(font[0])
        id = QFontDatabase.addApplicationFont("./fonts/NotoSansKR-Bold.ttf")
        font = QFontDatabase.applicationFontFamilies(id)
        self.cFonts.append(font[0])
        id = QFontDatabase.addApplicationFont("./fonts/KoHo-Bold.ttf")
        font = QFontDatabase.applicationFontFamilies(id)
        self.cFonts.append(font[0])
        print(self.cFonts)
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

        ################################################################################################
        # 광규 작성 부분
        # df0 = pd.read_csv('./menus/List_shrimp.csv', index_col=0).iloc[:,0]
        # df1 = pd.read_csv('./menus/List_squid.csv', index_col=0).iloc[:,0]
        # df2 = pd.read_csv('./menus/List_fish.csv', index_col=0).iloc[:,0]
        # df3 = pd.read_csv('./menus/List_meat.csv', index_col=0).iloc[:,0]
        # df4 = pd.read_csv('./menus/List_other.csv', index_col=0).iloc[:,0]
        # self.df_menu = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
        # self.df_cnt_db = np.zeros((len(self.df_menu), 5))
        # self.df_cnt = pd.DataFrame(self.df_cnt_db, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
        # self.df_position = pd.DataFrame(index=range(0, 100), columns=['menu_row', 'menu_col'])  # 메뉴확인 df와 table 위치확인
        ################################################################################################
        ################################################################################################
        # 성희 작성 부분
        self.menus_tot = [pd.read_csv('./menus/List_shrimp.csv'), pd.read_csv('./menus/List_squid.csv'),
               pd.read_csv('./menus/List_fish.csv'), pd.read_csv('./menus/List_meat.csv'), pd.read_csv('./menus/List_other.csv')]
        # self.df_menu = pd.concat(self.menus_tot, ignore_index=True)
        # self.df_cnt_db = np.zeros((len(self.df_menu), 4))  # 언어가 4개이므로
        # self.df_cnt = pd.DataFrame(self.df_cnt_db, columns=['Korea', 'English', 'Vietnam', 'Thailand'])  # 메뉴수량 df
        df0 = pd.read_csv('./menus/List_shrimp.csv').iloc[:, 0]
        df1 = pd.read_csv('./menus/List_squid.csv').iloc[:, 0]
        df2 = pd.read_csv('./menus/List_fish.csv').iloc[:, 0]
        df3 = pd.read_csv('./menus/List_meat.csv').iloc[:, 0]
        df4 = pd.read_csv('./menus/List_other.csv').iloc[:, 0]
        self.df_menu_kor = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
        df0 = pd.read_csv('./menus/List_shrimp.csv').iloc[:, 1]
        df1 = pd.read_csv('./menus/List_squid.csv').iloc[:, 1]
        df2 = pd.read_csv('./menus/List_fish.csv').iloc[:, 1]
        df3 = pd.read_csv('./menus/List_meat.csv').iloc[:, 1]
        df4 = pd.read_csv('./menus/List_other.csv').iloc[:, 1]
        self.df_menu_en = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
        df0 = pd.read_csv('./menus/List_shrimp.csv').iloc[:, 2]
        df1 = pd.read_csv('./menus/List_squid.csv').iloc[:, 2]
        df2 = pd.read_csv('./menus/List_fish.csv').iloc[:, 2]
        df3 = pd.read_csv('./menus/List_meat.csv').iloc[:, 2]
        df4 = pd.read_csv('./menus/List_other.csv').iloc[:, 2]
        self.df_menu_v = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
        df0 = pd.read_csv('./menus/List_shrimp.csv').iloc[:, 3]
        df1 = pd.read_csv('./menus/List_squid.csv').iloc[:, 3]
        df2 = pd.read_csv('./menus/List_fish.csv').iloc[:, 3]
        df3 = pd.read_csv('./menus/List_meat.csv').iloc[:, 3]
        df4 = pd.read_csv('./menus/List_other.csv').iloc[:, 3]
        self.df_menu_th = pd.concat([df0, df1, df2, df3, df4], axis=1, keys=['shrimp', 'squid', 'fish', 'meat', 'other'])
        self.df_menu = [self.df_menu_kor, self.df_menu_en, self.df_menu_v, self.df_menu_th]
        self.df_cnt_default0 = np.zeros((len(self.df_menu_kor), 5))
        self.df_cnt_default1 = np.zeros((len(self.df_menu_en), 5))
        self.df_cnt_default2 = np.zeros((len(self.df_menu_v), 5))
        self.df_cnt_default3 = np.zeros((len(self.df_menu_th), 5))
        self.df_cnt_kor = pd.DataFrame(self.df_cnt_default0, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
        self.df_cnt_en = pd.DataFrame(self.df_cnt_default1, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
        self.df_cnt_v = pd.DataFrame(self.df_cnt_default2, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
        self.df_cnt_th = pd.DataFrame(self.df_cnt_default3, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
        self.df_cnt = list([self.df_cnt_kor, self.df_cnt_en, self.df_cnt_v, self.df_cnt_th])

        self.df_position = pd.DataFrame(index=range(0, 100), columns=['menu_row', 'menu_col'])  # 메뉴확인 df와 table 위치확인
        ################################################################################################

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

        #####################################################################################
        # 폰트 설정
        self.tabWidget.setFont(QFont(self.cFonts[0], 12))
        self.tabWidget_2.setFont(QFont(self.cFonts[1], 11))
        self.label.setFont(QFont(self.cFonts[0], 11))
        font_t = QFont(self.cFonts[0], 11)
        font_t.setBold(True)
        # self.L1_table_btn.setFont(QFont(self.cFonts[0], 11).setBold(True))
        self.L1_table_btn.setFont(font_t)
        self.L2_btn.setFont(QFont(self.cFonts[0], 11))
        self.label_2.setFont(QFont(self.cFonts[0], 11))
        self.comboBox.setFont(QFont(self.cFonts[0], 8))
        self.menu.setFont(QFont(self.cFonts[0], 8))
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
        self.makeBtns(0)

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

    def makeBtns(self, langIdx):
        lang = ['Korea', 'English', 'Vietnam', 'Thailand']
        self.clearButtons()
        # 버튼 생성 및 배치
        gridlayouts = [self.gridlayout0, self.gridlayout1, self.gridlayout2, self.gridlayout3, self.gridlayout4]

        for df, gridlayout in zip(self.menus_tot, gridlayouts):
            for i, row in df.iterrows():
                text = row[lang[langIdx]]
                if '-' in text:
                    text = '\n'.join(text.split('-'))
                button = QPushButton(text)
                button.setStyleSheet(self.style_sheet_btn)
                button.setFont(QFont(self.cFonts[langIdx], 8))
                button.clicked.connect(lambda checked, btn=text, idx=i: self.buttonClicked(btn, idx))
                row = i // 4
                col = i % 4
                gridlayout.addWidget(button, row, col)
            spacer = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)  # vertical spacer 생성
            gridlayout.addItem(spacer, row + 1, 0, 1, 4)

    def clearButtons(self):
        gridlayouts = [self.gridlayout0, self.gridlayout1, self.gridlayout2, self.gridlayout3, self.gridlayout4]

        for gridlayout in gridlayouts:
            while gridlayout.count():
                item = gridlayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def buttonClicked(self, menu, menu_i):
        tabIdx = self.tabWidget_2.currentIndex()
        tab_name=self.tabWidget_2.tabText(tabIdx)
        self.L1_tableq(tabIdx, tab_name, menu, menu_i)

    def comboBoxTextChanged(self, text):
        lang = ['한국어', '영어', '베트남', '태국']
        self.lang_idx = lang.index(text)
        self.makeBtns(self.lang_idx)
    ############################################################################################################
    # 광규 작성
    '''
    def L1_tableq(self, tab, tab_name, menu, menu_i): # table 상태창
        menu_duplicate = 0  # menu중복확인
        self.df_cnt.iat[menu_i, tab] += 1  # menu 수량 추가
        self.currentRowCount = self.L1_table.rowCount()  # 현재 행 수 확인

        # table에 선택된 메뉴 존재여부 확인
        for i in range(self.currentRowCount):
            if self.L1_table.item(i, 0) == None:
                pass
            else:
                if tab_name == self.L1_table.item(i, 0).text():
                    if self.df_menu.iat[menu_i, tab] == self.L1_table.item(i, 1).text():
                        menu_duplicate = 1
                        check_row = i
                    else:
                        pass
                else:
                    pass
        if menu_duplicate == 1:
            self.L1_table.setItem(check_row, 0,QTableWidgetItem(str(tab_name)))  # table에 내용 update
            self.L1_table.setItem(check_row, 1, QTableWidgetItem(str(self.df_menu.iat[menu_i, tab])))  # table에 내용 update
            self.L1_table.setItem(check_row, 2,QTableWidgetItem(str(int(self.df_cnt.iat[menu_i, tab]))))  # table에 cnt update
            self.L1_table.setItem(check_row, 3, QTableWidgetItem('+'))  # table cnt 추가
            self.L1_table.setItem(check_row, 4, QTableWidgetItem('-'))  # table cnt 감소
            self.L1_table.setItem(check_row, 5, QTableWidgetItem('del'))  # table row 삭제
            self.df_position.iat[check_row, 0] = tab
            self.df_position.iat[check_row, 1] = menu_i
        else:
            if self.L1_table.item(0, 0) == None:
                self.L1_table.setItem(0, 0,QTableWidgetItem(str(tab_name)))  # table에 내용 update
                self.L1_table.setItem(0, 1, QTableWidgetItem(str(self.df_menu.iat[menu_i, tab])))  # table에 내용 update
                self.L1_table.setItem(0, 2, QTableWidgetItem(str(int(self.df_cnt.iat[menu_i, tab]))))  # table에 cnt update
                self.L1_table.setItem(0, 3, QTableWidgetItem('+'))  # table cnt 추가
                self.L1_table.setItem(0, 4, QTableWidgetItem('-'))  # table cnt 감소
                self.L1_table.setItem(0, 5, QTableWidgetItem('del'))  # table row 삭제
                self.df_position.iat[0, 0] = tab
                self.df_position.iat[0, 1] = menu_i
            else:
                self.L1_table.insertRow(self.currentRowCount)  # 행 추가
                self.L1_table.setItem(self.currentRowCount, 0,QTableWidgetItem(str(tab_name)))  # table에 내용 update
                self.L1_table.setItem(self.currentRowCount, 1,QTableWidgetItem(str(self.df_menu.iat[menu_i, tab])))  # table에 내용 update
                self.L1_table.setItem(self.currentRowCount, 2,QTableWidgetItem(str(int(self.df_cnt.iat[menu_i, tab]))))  # table에 cnt update
                self.L1_table.setItem(self.currentRowCount, 3, QTableWidgetItem('+'))  # table cnt 추가
                self.L1_table.setItem(self.currentRowCount, 4, QTableWidgetItem('-'))  # table cnt 감소
                self.L1_table.setItem(self.currentRowCount, 5, QTableWidgetItem('del'))  # table row 삭제
                self.df_position.iat[self.currentRowCount, 0] = tab
                self.df_position.iat[self.currentRowCount, 1] = menu_i
    '''
    ######################################################################################################################

    #####################################################################################################################
    # 성희 작성
    def L1_tableq(self, tab, tab_name, menu, menu_i): # table 상태창
        menu_duplicate = 0  # menu중복확인
        self.df_cnt[self.lang_idx].iat[menu_i, tab] += 1  # menu 수량 추가
        self.currentRowCount = self.L1_table.rowCount()  # 현재 행 수 확인

        # table에 선택된 메뉴 존재여부 확인
        for i in range(self.currentRowCount):
            if self.L1_table.item(i, 0) == None:
                pass
            else:
                if tab_name == self.L1_table.item(i, 0).text():
                    if self.df_menu[self.lang_idx].iat[menu_i, tab] == self.L1_table.item(i, 1).text():
                        menu_duplicate = 1
                        check_row = i
                    else:
                        pass
                else:
                    pass
        if menu_duplicate == 1:
            self.L1_table.setItem(check_row, 0, QTableWidgetItem(str(tab_name)))  # table에 내용 update
            self.L1_table.setItem(check_row, 1, QTableWidgetItem(str(self.df_menu[self.lang_idx].iat[menu_i, tab])))  # table에 내용 update
            self.L1_table.setItem(check_row, 2, QTableWidgetItem(str(int(self.df_cnt[self.lang_idx].iat[menu_i, tab]))))  # table에 cnt update
            self.L1_table.setItem(check_row, 3, QTableWidgetItem('+'))  # table cnt 추가
            self.L1_table.setItem(check_row, 4, QTableWidgetItem('-'))  # table cnt 감소
            self.L1_table.setItem(check_row, 5, QTableWidgetItem('del'))  # table row 삭제
            self.df_position.iat[check_row, 0] = tab
            self.df_position.iat[check_row, 1] = menu_i
        else:
            if self.L1_table.item(0, 0) == None:
                self.L1_table.setItem(0, 0,QTableWidgetItem(str(tab_name)))  # table에 내용 update
                self.L1_table.setItem(0, 1, QTableWidgetItem(str(self.df_menu[self.lang_idx].iat[menu_i, tab])))  # table에 내용 update
                self.L1_table.setItem(0, 2, QTableWidgetItem(str(int(self.df_cnt[self.lang_idx].iat[menu_i, tab]))))  # table에 cnt update
                self.L1_table.setItem(0, 3, QTableWidgetItem('+'))  # table cnt 추가
                self.L1_table.setItem(0, 4, QTableWidgetItem('-'))  # table cnt 감소
                self.L1_table.setItem(0, 5, QTableWidgetItem('del'))  # table row 삭제
                self.df_position.iat[0, 0] = tab
                self.df_position.iat[0, 1] = menu_i
            else:
                self.L1_table.insertRow(self.currentRowCount)  # 행 추가
                self.L1_table.setItem(self.currentRowCount, 0,QTableWidgetItem(str(tab_name)))  # table에 내용 update
                self.L1_table.setItem(self.currentRowCount, 1,QTableWidgetItem(str(self.df_menu[self.lang_idx].iat[menu_i, tab])))  # table에 내용 update
                self.L1_table.setItem(self.currentRowCount, 2,QTableWidgetItem(str(int(self.df_cnt[self.lang_idx].iat[menu_i, tab]))))  # table에 cnt update
                self.L1_table.setItem(self.currentRowCount, 3, QTableWidgetItem('+'))  # table cnt 추가
                self.L1_table.setItem(self.currentRowCount, 4, QTableWidgetItem('-'))  # table cnt 감소
                self.L1_table.setItem(self.currentRowCount, 5, QTableWidgetItem('del'))  # table row 삭제
                self.df_position.iat[self.currentRowCount, 0] = tab
                self.df_position.iat[self.currentRowCount, 1] = menu_i
    #####################################################################################################################
    def L1_table_editq(self):
        selected_box = self.L1_table.selectedIndexes()  # 선택된 좌표값 받아오기
        # print(selected_box[0].row())  #int
        # print(selected_box[0].column())  #int

        if selected_box[0].column() == 3:  # 수량 +
            print('test')
            add_df_row = self.df_position.iat[selected_box[0].row(), 0]
            print('a')
            add_df_col = self.df_position.iat[selected_box[0].row(), 1]
            print('b')
            self.df_cnt[self.lang_idx].iat[add_df_col, add_df_row] += 1
            print('c')
            self.L1_table.setItem(selected_box[0].row(), 2, QTableWidgetItem(str(int(self.df_cnt[self.lang_idx].iat[add_df_col, add_df_row]))))  # table에 cnt update
            print('d')

        if selected_box[0].column() == 4:  # 수량 -
            sub_df_row = self.df_position.iat[selected_box[0].row(), 0]
            sub_df_col = self.df_position.iat[selected_box[0].row(), 1]
            if self.df_cnt[self.lang_idx].iat[sub_df_col, sub_df_row] == 1:
                pass
            else:
                self.df_cnt[self.lang_idx].iat[sub_df_col, sub_df_row] -= 1
                self.L1_table.setItem(selected_box[0].row(), 2, QTableWidgetItem(str(int(self.df_cnt[self.lang_idx].iat[sub_df_col, sub_df_row]))))  # table에 cnt update

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
            if RowLeft == 1:
                self.df_cnt_kor = pd.DataFrame(self.df_cnt_default0,
                                               columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
                self.df_cnt_en = pd.DataFrame(self.df_cnt_default1,
                                              columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
                self.df_cnt_v = pd.DataFrame(self.df_cnt_default2, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
                self.df_cnt_th = pd.DataFrame(self.df_cnt_default3,
                                              columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
                self.df_cnt = list([self.df_cnt_kor, self.df_cnt_en, self.df_cnt_v, self.df_cnt_th])
                for col in range(5):
                    self.L1_table.setItem(0, col, None)  # 빈칸표시
            else:
                self.L1_table.removeRow(selected_box[0].row()) # 선택된 행 삭제
                del_df_row=self.df_position.iat[selected_box[0].row(), 0]
                del_df_col=self.df_position.iat[selected_box[0].row(), 1]
                self.df_cnt[self.lang_idx].iat[del_df_col, del_df_row] = 0  # 선택된 menu 수량 삭제
                self.df_position.drop(selected_box[0].row(), axis=0, inplace=True)
                self.df_position.loc['100']= [np.nan,np.nan]
                self.df_position.reset_index(inplace=True,drop=True)


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
        data_df = pd.DataFrame()# index=range(0, 100), columns=['menu_category', 'menu_item','menu_cnt'])
        if self.L1_table.item(0, 0) == None:
            pass
        else:
            cnt_tot = pd.concat(self.df_cnt)
            sum_df = cnt_tot.groupby(level=0).sum()
            print(sum_df)

            orderlist = []
            for i in range(len(sum_df)):
                for j in range(len(sum_df.columns)):
                    if sum_df.iloc[i, j] != 0:
                        orderlist.append((i, j, sum_df.iloc[i, j]))

            print(orderlist)


            data_dict = {}
            for row in range(self.L1_table.rowCount()):
                menu_category = self.L1_table.item(row, 0).text()
                menu_item = self.L1_table.item(row, 1).text()
                menu_cnt = self.L1_table.item(row, 2).text()
                data_dict[menu_item] = menu_cnt
                data=pd.DataFrame({'menu_category': [menu_category], 'menu_item': [menu_item], 'menu_cnt': [menu_cnt]})
                data_df = pd.concat([data_df, data], ignore_index=True)
            items = []
            for index, row in data_df.iterrows():
                # item = f"{row['menu_category']}_{row['menu_item']}{row['menu_cnt']}, "
                item = f"{row['menu_item']}{row['menu_cnt']}, "
                items.append(item)
            combined_items = ''.join(items)
            #######################################################################################
            # 맨 끝 콤마 삭제
            combined_items = combined_items[:-2]
            #######################################################################################
            self.L2_text.setPlainText(combined_items)
            # self.df_cnt = pd.DataFrame(np.zeros((len(self.df_menu), 5)), columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
            self.df_cnt_kor = pd.DataFrame(self.df_cnt_default0,
                                           columns=['shrimp', 'squid', 'fish', 'meat', 'other'])  # 메뉴수량 df
            self.df_cnt_en = pd.DataFrame(self.df_cnt_default1, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
            self.df_cnt_v = pd.DataFrame(self.df_cnt_default2, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
            self.df_cnt_th = pd.DataFrame(self.df_cnt_default3, columns=['shrimp', 'squid', 'fish', 'meat', 'other'])
            self.df_cnt = list([self.df_cnt_kor, self.df_cnt_en, self.df_cnt_v, self.df_cnt_th])
            self.df_position = pd.DataFrame(index=range(0, 100),columns=['menu_row', 'menu_col'])  # 메뉴확인 df와 table 위치확인

            self.L1_table.setRowCount(1)  # row 삭제
            self.L1_table.setColumnCount(6)  #column 6개
            self.L1_table.setHorizontalHeaderLabels(['카테고리', '주문메뉴','수량','+', '-', '삭제'])  # column 입력
            self.L1_table.setColumnWidth(0, int((self.L1_table.width() - 20) * 2.5 / 10))  # 메뉴
            self.L1_table.setColumnWidth(1, int((self.L1_table.width() - 20) * 3.5 / 10))  # 메뉴
            self.L1_table.setColumnWidth(2, int((self.L1_table.width() - 20) * 1 / 10))  # 수량
            self.L1_table.setColumnWidth(3, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량추가
            self.L1_table.setColumnWidth(4, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량감소
            self.L1_table.setColumnWidth(5, int((self.L1_table.width() - 20) * 0.5 / 10))  # 수량삭제
            for col in range(6):
                self.L1_table.setItem(0, col, None) #빈칸표시
    def L2_btnq(self):  # History저장
        if self.user == None:
            director='director'
        else:
            director=self.user

        if self.L2_text.toPlainText() == '':
            pass
        else:
            print(self.L2_text.toPlainText())
            ##############################################################################
            ## 클립보드에 복사 코드
            clipboard = QApplication.clipboard()
            clipboard.setText(self.L2_text.toPlainText())
            ##############################################################################
            currentRowCount = self.L2_table.rowCount()  # 현재 행 수 확인
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d  %H:%M:%S")
            if self.L2_table.item(0, 0) == None:
                self.L2_table.setItem(0, 0, QTableWidgetItem(str(formatted_date)))  # table에 내용 update
                self.L2_table.setItem(0, 1, QTableWidgetItem(str(director)))  # table에 내용 update
                self.L2_table.setItem(0, 2, QTableWidgetItem(str(self.L2_text.toPlainText())))  # table에 cnt update
            else:
                self.L2_table.insertRow(currentRowCount)  # 행 추가
                self.L2_table.setItem(currentRowCount, 0,QTableWidgetItem(str(formatted_date)))  # table에 내용 update
                self.L2_table.setItem(currentRowCount, 1,QTableWidgetItem(str(director)))  # table에 내용 update
                self.L2_table.setItem(currentRowCount, 2,QTableWidgetItem(str(self.L2_text.toPlainText())))  # table에 cnt update

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
            self.L2_text.clear()
            # 추출한 데이터를 Pandas DataFrame으로 변환
            order_data_df = pd.DataFrame(order_data, columns=['time', 'Director', 'Order History'])
            with open(os.getcwd() + '\Order_History.csv', 'w', newline="", encoding='utf-8') as csvfile:
                order_data_df.to_csv(csvfile, header=csvfile.tell() == 0)  # 존재하지 않는 경우, 파일 생성, 있으면 내용 추가

if __name__=="__main__":  # 프로그램 실행
    app = QApplication(sys.argv)
    myWindow=MyWindow()   # MyWindow 함수 변수화
    myWindow.show()  # Window 화면 실행
    app.exec_()  # 이벤트 loop 실행

