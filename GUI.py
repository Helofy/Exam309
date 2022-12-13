from PyQt5.QtWidgets import *
import threading

import sys

import Client
from PyQt5 import QtGui

class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QtGui.QIcon('logo.png'))# mise en place du logo en haut à gauche
        self.Machine=Client.Client('localhost',10000)
        self.i = 0
        self.setWindowTitle("Un logociel de tchat")
        self.resize(300, 270)

        self.Host=QLabel('serveur - port :')
        self.Hostip=QLineEdit('localhost')
        self.Portnum = QLineEdit('10000')
        self.Status=QLabel('Disconnected')
        self.btnconn = QPushButton("Connexion")
        self.btnquit=QPushButton("Quit")
        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(False)
        self.btnPress1 = QPushButton("Envoyé")
        self.btnPress1.setEnabled(False)
        self.btnPress2 = QPushButton("Effacer")

        self.message = QTextEdit()
        self.message.setEnabled(False)

        layout = QGridLayout()
        layout.addWidget(self.Host,0,0,1,1)
        layout.addWidget(self.Hostip,0,1,1,2)
        layout.addWidget(self.Portnum,0,2,1,1)
        layout.addWidget(self.btnconn ,0,3,1,1)
        layout.addWidget(self.btnquit,1,2,1,1)
        layout.addWidget(self.Status,1,0,1,2)

        layout.addWidget(self.textEdit,2,0,2,8)
        layout.addWidget(self.btnPress1)
        layout.addWidget((self.message))
        layout.addWidget(self.btnPress2)

        self.setLayout(layout)
        self.btnconn.clicked.connect(self.connexion)
        self.btnquit.clicked.connect(self.quit)
        self.btnPress1.clicked.connect(self.btnPress1_Clicked)
        self.btnPress2.clicked.connect(self.btnPress2_Clicked)


    def quit(self):
        if self.Status.text()=='Connected':
            self.Machine.envoi('deco-server')
            self.Machine.disconnect()
        else:
                msg = QMessageBox()
                msg.setWindowTitle("Pas connecter")
                msg.setText("Il n'y a pas de connexion ")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()






    def reception(self):
        msg = ""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.Machine.reception()
            self.textEdit.append(msg)
            print(msg)

    def connexion(self):
        if self.btnconn.text() !='Déconnexion':
            host=str(self.Hostip.text())
            port=int(self.Portnum.text())
            self.Machine = Client.Client(host,port)
            try:
                a=self.Machine.connect()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText("Conexion erreur")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

            else:

                if int(a) != -1:

                    self.Status.setText('Connected')
                    self.message.setEnabled(True)
                    self.btnPress2.setEnabled(True)
                    self.btnPress1.setEnabled(True)
                    self.Hostip.setEnabled(True)
                    self.Portnum.setEnabled(False)

                    self.btnconn.setText('Déconnexion')

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Erreur")
                    msg.setText('Le serveur est non lancé ou les information mauvaise !!')
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
        else:
            try:
                self.Machine.envoi('deco-server')
                self.Machine.disconnect()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText("déconextion du serveur")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            self.Host.setEnabled(True)
            self.Portnum.setEnabled(True)
            self.message.setEnabled(False)
            self.btnPress2.setEnabled(False)
            self.btnPress1.setEnabled(False)
            self.Status.setText('Disconnected')
            self.btnconn.setText('Connexion')

    #        self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

    def btnPress1_Clicked(self,Machine):

        if self.Status.text()!='Disconnected':
            text=self.message.toPlainText()
            try:
                self.Machine.envoi(text)
                self.textEdit.append(text)
            except :
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText("erreur message")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Le client n'est pas connecter au serveur")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def btnPress2_Clicked(self):
        self.textEdit.setPlainText("")
#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())