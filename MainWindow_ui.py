# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Fri Jan 06 06:25:12 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(691, 407)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 691, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAccounts = QtGui.QMenu(self.menubar)
        self.menuAccounts.setObjectName(_fromUtf8("menuAccounts"))
        self.menuBackpack = QtGui.QMenu(self.menubar)
        self.menuBackpack.setObjectName(_fromUtf8("menuBackpack"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setShortcut(_fromUtf8("Ctrl+Q"))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionCheck_for_update = QtGui.QAction(MainWindow)
        self.actionCheck_for_update.setObjectName(_fromUtf8("actionCheck_for_update"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAdd_account = QtGui.QAction(MainWindow)
        self.actionAdd_account.setObjectName(_fromUtf8("actionAdd_account"))
        self.menuFile.addAction(self.actionExit)
        self.menuAccounts.addAction(self.actionAdd_account)
        self.menuAccounts.addSeparator()
        self.menuAbout.addAction(self.actionCheck_for_update)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAccounts.menuAction())
        self.menubar.addAction(self.menuBackpack.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAccounts.setTitle(QtGui.QApplication.translate("MainWindow", "Accounts", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBackpack.setTitle(QtGui.QApplication.translate("MainWindow", "Backpack", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setToolTip(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Exit TF2Idle", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCheck_for_update.setText(QtGui.QApplication.translate("MainWindow", "Check for update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_account.setText(QtGui.QApplication.translate("MainWindow", "Add account", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_account.setStatusTip(QtGui.QApplication.translate("MainWindow", "Add a Steam account", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_account.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))

