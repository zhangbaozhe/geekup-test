from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QImage
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import sys
import binascii


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = QPixmap(pixmap).scaled(64, 64)

        self.image = QImage()
        self.image.load(pixmap)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(500, 425)
        self.setUi()
        self.signalSlot()
        self.refresh()

        self.encoding = "utf-8"

    def setUi(self):
        self.mainLayout = QGridLayout()

        self.com_comboBox = QComboBox()
        self.com_button = QPushButton("Open COM Port")
        self.refresh_button = QPushButton("Refresh")
        self.model_label = QLabel("Control Model")
        self.cmd_button = QPushButton("CMD Control")
        self.gui_button = QPushButton("GUI Control")
        self.rmt_button = QPushButton("RMT Control")

        self.layout1 = QGridLayout()
        self.layout1.addWidget(self.com_comboBox, 0, 0, 1, 2)
        self.layout1.addWidget(self.com_button, 1, 0, 1, 1)
        self.layout1.addWidget(self.refresh_button, 1, 1, 1, 1)
        self.layout1.addWidget(self.model_label, 2, 0, 1, 2)
        self.layout1.addWidget(self.cmd_button, 3, 0, 1, 2)
        self.layout1.addWidget(self.gui_button, 4, 0, 1, 2)
        self.layout1.addWidget(self.rmt_button, 5, 0, 1, 2)
        self.mainLayout.addLayout(self.layout1, 0, 0, 2, 1)

        self.up_picButton = PicButton("up.png")
        self.left_picButton = PicButton("left.png")
        self.right_picButton = PicButton("right.png")
        self.down_picButton = PicButton("down.png")


        self.layout2 = QGridLayout()
        self.layout2.addWidget(self.up_picButton, 0, 1, 1, 1)
        self.layout2.addWidget(self.left_picButton, 1, 0, 1, 1)
        self.layout2.addWidget(self.right_picButton, 1, 2, 1, 1)
        self.layout2.addWidget(self.down_picButton, 2, 1, 1, 1)
        self.mainLayout.addLayout(self.layout2, 0, 1, 1, 1)

        self.rudder_label = QLabel("Rudder Angle")
        self.rudder_spinBox = QSpinBox()
        self.fan_label = QLabel("Fan Angle")
        self.fan_spinBox = QSpinBox()

        self.layout3 = QGridLayout()
        self.layout3.addWidget(self.rudder_label, 0, 0, 1, 1)
        self.layout3.addWidget(self.rudder_spinBox, 0, 1, 1, 1)
        self.layout3.addWidget(self.fan_label, 1, 0, 1, 1)
        self.layout3.addWidget(self.fan_spinBox, 1, 1, 1, 1)
        self.mainLayout.addLayout(self.layout3, 1, 1, 1, 1)

        self.textEdit = QTextEdit()
        self.send_button = QPushButton("Send")

        self.layout4 = QGridLayout()
        self.layout4.addWidget(self.textEdit, 0, 0, 1, 2)
        self.layout4.addWidget(self.send_button, 0, 2, 1, 1)
        self.mainLayout.addLayout(self.layout4, 2, 0, 1, 2)


        self.setLayout(self.mainLayout)

    def signalSlot(self):
        self.com_button.clicked.connect(self.openCOM)
        self.refresh_button.clicked.connect(self.refresh)
        self.cmd_button.clicked.connect(self.cmdControl)
        self.gui_button.clicked.connect(self.guiControl)
        self.rmt_button.clicked.connect(self.rmtControl)
        self.up_picButton.clicked.connect(self.up)
        self.down_picButton.clicked.connect(self.down)
        self.right_picButton.clicked.connect(self.right)
        self.left_picButton.clicked.connect(self.left)
        self.send_button.clicked.connect(self.send)
        self.rudder_spinBox.editingFinished.connect(self.rudder)
        self.fan_spinBox.editingFinished.connect(self.fan)

    def openCOM(self):
        if self.com_button.text()=="Open COM Port":
            if self.com_comboBox.currentText() != None:

                com_name = self.com_comboBox.currentText()
                com_baudrate = 19200

                self.com = QSerialPort()
                self.com.setPortName(com_name)

            try:
                if self.com.open(QSerialPort.WriteOnly) == False:
                    QMessageBox.critical(self, "ERROR", "Failed Opening COM", buttons=QMessageBox.Ok)
                    return
            except:
                print("except")
                QMessageBox.critical(self, "ERROR", "Failed Opening COM", buttons=QMessageBox.Ok)
                return

            if self.com.isOpen():
                self.com.setBaudRate(com_baudrate)
                self.com_button.setText("Close COM port")
        else:
            if self.com.isOpen():
                self.com.close()
                self.com_button.setText("Open COM Port")

    def refresh(self):
        self.com_comboBox.clear()
        com = QSerialPort()
        for info in QSerialPortInfo.availablePorts():
            com.setPort(info)
            if com.open(QSerialPort.WriteOnly):
                self.com_comboBox.addItem(info.portName())
                com.close()

        pass

    def cmdControl(self):
        self.gui_button.setEnabled(False)
        self.rmt_button.setEnabled(False)
        self.up_picButton.setEnabled(False)
        self.down_picButton.setEnabled(False)
        self.left_picButton.setEnabled(False)
        self.right_picButton.setEnabled(False)
        self.rudder_spinBox.setEnabled(False)
        self.fan_spinBox.setEnabled(False)
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("0101"))

        pass

    def guiControl(self):
        self.cmd_button.setEnabled(False)
        self.rmt_button.setEnabled(False)
        self.send_button.setEnabled(False)
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("0202"))
        pass

    def rmtControl(self):
        self.cmd_button.setEnabled(False)
        self.gui_button.setEnabled(False)
        self.rudder_spinBox.setEnabled(False)
        self.fan_spinBox.setEnabled(False)
        self.up_picButton.setEnabled(False)
        self.down_picButton.setEnabled(False)
        self.left_picButton.setEnabled(False)
        self.right_picButton.setEnabled(False)
        self.send_button.setEnabled(False)
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("1212"))
        pass

    def up(self):
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("31"))
#            fan = int(self.fan_spinBox.text())+1
            fan = "s"
            self.fan_spinBox.setSpecialValueText(str(fan))

        pass

    def down(self):
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("32"))
            fan = "j"
#            fan = int(self.fan_spinBox.text())+1
            self.fan_spinBox.setSpecialValueText(str(fan))


        pass

    def left(self):
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("33"))
            rudder = 'l'
#            rudder = int(self.rudder_spinBox.text())-6
            self.rudder_spinBox.setSpecialValueText(str(rudder))


        pass

    def right(self):
        if self.com.isOpen():
            self.com.write(binascii.a2b_hex("34"))
            rudder = 'r'
#            rudder = int(self.rudder_spinBox.text())+6
            self.rudder_spinBox.setSpecialValueText(str(rudder))


        pass

    def send(self):
        txt_data = self.textEdit.toPlainText()
        if len(txt_data) == 0:
            return
        data = txt_data.replace(" ", "")
        if len(data)%2 == 1:
            QMessageBox.critical(self, "ERROR", "Not Hex Numbers")
            return
        if not data.isalnum():
            QMessageBox.critical(self, "ERROR", "Including Non-hex Number")
            return
        try:
            hex_data = binascii.a2b_hex(data)
            print(hex_data)
            if self.com.isOpen():
                self.com.write(hex_data)
        except:
            QMessageBox.critical(self, "ERROR", "Failed Sending Data")

        pass

    def rudder(self):
        pass

    def fan(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
