# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainForm.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_mainForm(object):
    def setupUi(self, mainForm):
        if not mainForm.objectName():
            mainForm.setObjectName(u"mainForm")
        mainForm.resize(680, 682)
        self.centralwidget = QWidget(mainForm)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 90, 651, 51))
        self.layoutSimple = QHBoxLayout(self.horizontalLayoutWidget)
        self.layoutSimple.setObjectName(u"layoutSimple")
        self.layoutSimple.setContentsMargins(0, 0, 0, 0)
        self.lblUsername = QLabel(self.horizontalLayoutWidget)
        self.lblUsername.setObjectName(u"lblUsername")
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(12)
        self.lblUsername.setFont(font)

        self.layoutSimple.addWidget(self.lblUsername)

        self.txtUsername = QLineEdit(self.horizontalLayoutWidget)
        self.txtUsername.setObjectName(u"txtUsername")
        self.txtUsername.setFont(font)

        self.layoutSimple.addWidget(self.txtUsername)

        self.btnGoSimple = QPushButton(self.horizontalLayoutWidget)
        self.btnGoSimple.setObjectName(u"btnGoSimple")
        font1 = QFont()
        font1.setFamily(u"Calibri")
        font1.setPointSize(14)
        self.btnGoSimple.setFont(font1)

        self.layoutSimple.addWidget(self.btnGoSimple)

        self.lblSimpleMode = QLabel(self.centralwidget)
        self.lblSimpleMode.setObjectName(u"lblSimpleMode")
        self.lblSimpleMode.setGeometry(QRect(10, 60, 651, 41))
        self.lblSimpleMode.setFont(font)
        self.lblAdvanceMode = QLabel(self.centralwidget)
        self.lblAdvanceMode.setObjectName(u"lblAdvanceMode")
        self.lblAdvanceMode.setGeometry(QRect(10, 160, 651, 41))
        self.lblAdvanceMode.setFont(font)
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 200, 651, 281))
        self.layoutAdvance = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.layoutAdvance.setObjectName(u"layoutAdvance")
        self.layoutAdvance.setContentsMargins(0, 0, 0, 0)
        self.layoutToken = QVBoxLayout()
        self.layoutToken.setObjectName(u"layoutToken")
        self.lblToken = QLabel(self.horizontalLayoutWidget_2)
        self.lblToken.setObjectName(u"lblToken")
        self.lblToken.setFont(font)

        self.layoutToken.addWidget(self.lblToken)

        self.btnFetchToken = QPushButton(self.horizontalLayoutWidget_2)
        self.btnFetchToken.setObjectName(u"btnFetchToken")
        self.btnFetchToken.setFont(font1)

        self.layoutToken.addWidget(self.btnFetchToken)

        self.txtToken = QTextEdit(self.horizontalLayoutWidget_2)
        self.txtToken.setObjectName(u"txtToken")

        self.layoutToken.addWidget(self.txtToken)


        self.layoutAdvance.addLayout(self.layoutToken)

        self.btnGoAdvance = QPushButton(self.horizontalLayoutWidget_2)
        self.btnGoAdvance.setObjectName(u"btnGoAdvance")
        self.btnGoAdvance.setFont(font1)

        self.layoutAdvance.addWidget(self.btnGoAdvance)

        self.lblOthers = QLabel(self.centralwidget)
        self.lblOthers.setObjectName(u"lblOthers")
        self.lblOthers.setGeometry(QRect(10, 490, 651, 41))
        self.lblOthers.setFont(font)
        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 520, 651, 51))
        self.layoutTachi = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.layoutTachi.setObjectName(u"layoutTachi")
        self.layoutTachi.setContentsMargins(0, 0, 0, 0)
        self.lblTachi = QLabel(self.horizontalLayoutWidget_3)
        self.lblTachi.setObjectName(u"lblTachi")
        self.lblTachi.setFont(font)

        self.layoutTachi.addWidget(self.lblTachi)

        self.txtTachi = QLineEdit(self.horizontalLayoutWidget_3)
        self.txtTachi.setObjectName(u"txtTachi")
        self.txtTachi.setFont(font)

        self.layoutTachi.addWidget(self.txtTachi)

        self.lblStatus = QLabel(self.centralwidget)
        self.lblStatus.setObjectName(u"lblStatus")
        self.lblStatus.setGeometry(QRect(10, 0, 651, 41))
        self.lblStatus.setFont(font)
        self.lblGithubPage = QLabel(self.centralwidget)
        self.lblGithubPage.setObjectName(u"lblGithubPage")
        self.lblGithubPage.setGeometry(QRect(10, 600, 651, 41))
        self.lblGithubPage.setFont(font)
        self.lblGithubPage.setOpenExternalLinks(True)
        mainForm.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainForm)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 680, 26))
        mainForm.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainForm)
        self.statusbar.setObjectName(u"statusbar")
        mainForm.setStatusBar(self.statusbar)

        self.retranslateUi(mainForm)

        QMetaObject.connectSlotsByName(mainForm)
    # setupUi

    def retranslateUi(self, mainForm):
        mainForm.setWindowTitle(QCoreApplication.translate("mainForm", u"MainWindow", None))
#if QT_CONFIG(accessibility)
        mainForm.setAccessibleName(QCoreApplication.translate("mainForm", u"mainForm", None))
#endif // QT_CONFIG(accessibility)
        self.lblUsername.setText(QCoreApplication.translate("mainForm", u"Username: ", None))
#if QT_CONFIG(accessibility)
        self.txtUsername.setAccessibleName(QCoreApplication.translate("mainForm", u"txtUsername", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.btnGoSimple.setAccessibleName(QCoreApplication.translate("mainForm", u"btnGoSimple", None))
#endif // QT_CONFIG(accessibility)
        self.btnGoSimple.setText(QCoreApplication.translate("mainForm", u"Go!", None))
        self.lblSimpleMode.setText(QCoreApplication.translate("mainForm", u"Simple mode (Public list only)", None))
        self.lblAdvanceMode.setText(QCoreApplication.translate("mainForm", u"Advance mode (Includes Private Lists, needs oAuth token)", None))
        self.lblToken.setText(QCoreApplication.translate("mainForm", u"Token (from Web browser):", None))
#if QT_CONFIG(accessibility)
        self.btnFetchToken.setAccessibleName(QCoreApplication.translate("mainForm", u"btnFetchToken", None))
#endif // QT_CONFIG(accessibility)
        self.btnFetchToken.setText(QCoreApplication.translate("mainForm", u"Fetch Token", None))
#if QT_CONFIG(accessibility)
        self.txtToken.setAccessibleName(QCoreApplication.translate("mainForm", u"txtToken", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.btnGoAdvance.setAccessibleName(QCoreApplication.translate("mainForm", u"btnGoAdvance", None))
#endif // QT_CONFIG(accessibility)
        self.btnGoAdvance.setText(QCoreApplication.translate("mainForm", u"Go!", None))
        self.lblOthers.setText(QCoreApplication.translate("mainForm", u"Others", None))
        self.lblTachi.setText(QCoreApplication.translate("mainForm", u"Tachiyomi Backup:", None))
#if QT_CONFIG(accessibility)
        self.txtTachi.setAccessibleName(QCoreApplication.translate("mainForm", u"txtTachi", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.lblStatus.setAccessibleName(QCoreApplication.translate("mainForm", u"lblStatus", None))
#endif // QT_CONFIG(accessibility)
        self.lblStatus.setText(QCoreApplication.translate("mainForm", u"Status: ", None))
#if QT_CONFIG(accessibility)
        self.lblGithubPage.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.lblGithubPage.setText(QCoreApplication.translate("mainForm", u"View Github Page", None))
    # retranslateUi

