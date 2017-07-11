#!/usr/bin/env python3
# coding=utf-8

from socket import *
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

class Asker(QThread):
    def __init__(self, sock, list_widget):
        super(Asker, self).__init__()
        self.sock = sock
        self.list_widget = list_widget
    def __del__(self):
        self.wait()
    def run(self):
        while True:
            try:
                got = self.sock.recvfrom(1024)[0].decode()
                self.list_widget.addItem(got)
            except:
                pass

class QtClient(QMainWindow):
    def __init__(self):
        super(QtClient, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setblocking(False)
        ok = False
        while not ok:
            self.server_ip, ok = QInputDialog.getText(self, "Server IP", "Input server IP:")
            try:
                self.sock.sendto(b"_Init_", (self.server_ip, 8080))
            except:
                QMessageBox.warning(self, "Error", "Cannot connect to server. Check server IP and try again.", QMessageBox.Ok, QMessageBox.Ok)
                ok = False
        ok = False
        while not ok:
            self.name, ok = QInputDialog.getText(self, "Your name", "Name yourself:")
        self.init_ui()
    def init_ui(self):
        self.recv = QListWidget()
        self.send = QLineEdit()
        self.send.returnPressed.connect(self.send_text)
        layout_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.recv)
        layout.addWidget(self.send)
        layout_widget.setLayout(layout)
        self.setCentralWidget(layout_widget)
        save_as_action = QAction("Save &as...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setStatusTip("Save chat as...")
        save_as_action.triggered.connect(self.save_as_event)
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit chat")
        exit_action.triggered.connect(qApp.quit)
        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)
        thr = Asker(self.sock, self.recv)
        thr.start()
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle("Chat")
        self.show()
    def send_text(self):
        text = self.send.text()
        if text:
            self.sock.sendto(self.name.encode() + b"): " + text.encode(), (self.server_ip, 8080))
            self.send.clear()
            self.recv.addItem("(" + self.name + "): " + text)
    def save_as_event(self):
        filename = QFileDialog.getSaveFileName(self, "Save as...")[0]
        if not filename:
            return
        items = []
        for i in range(self.recv.count()):
            items.append(self.recv.item(i))
        try:
            with open(filename, "w") as f:
                for item in items:
                    f.write(item.text() + "\n")
        except:
            QMessageBox.warning(self, "Error", "Cannot save as " + filename, QMessageBox.Ok, QMessageBox.Ok)
            return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = QtClient()
    sys.exit(app.exec_())
