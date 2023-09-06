def makeBtns(self, langIdx):
    lang = ['Korea', 'English', 'Vietnam', 'Thailand']
    self.clearButtons()
    # 버튼 생성 및 배치
    dfs = [pd.read_csv('./menus/List_shrimp.csv', encoding='utf-8'), pd.read_csv('./menus/List_squid.csv'), pd.read_csv('./menus/List_fish.csv'),
           pd.read_csv('./menus/List_meat.csv'), pd.read_csv('./menus/List_other.csv')]
    gridlayouts = [self.gridlayout0, self.gridlayout1, self.gridlayout2, self.gridlayout3, self.gridlayout4]

    for df, gridlayout in zip(dfs, gridlayouts):
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