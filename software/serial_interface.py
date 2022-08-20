
from PySide2.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide2.QtCore import QIODevice


class SerialInterface:

    DEFAULT_BAUND_RATE = 115200

    def __init__(self):
        self.port_l = []
        self.port_name_l = []
        self.bauds_l = []
        self.serial_port = QSerialPort()

    def get_default_baund_rate(self):
        if self.DEFAULT_BAUND_RATE in self.bauds_l:
            return self.DEFAULT_BAUND_RATE
        else:
            return self.bauds_l[-1]

    def refresh_com_list(self):
        """Return serial port list."""
        port_l = QSerialPortInfo().availablePorts()
        port_name_l = [port.portName() for port in port_l]
        port_name_l.sort()
        bauds_l = port_l[0].standardBaudRates()
        port_l.reverse()
        port_name_l.reverse()
        self.port_l = port_l
        self.port_name_l = port_name_l
        self.bauds_l = bauds_l

    def load_baund_rate_from_port(self, port_name):
        if port_name in self.port_name_l:
            p = self.port_l[self.port_name_l.index(port_name)]
            self.bauds_l = p.standardBaudRates()

    def open_serial_port(self, port, baund):
        # port = window.com_cb.currentText()
        serial_port = self.serial_port
        try:
            serial_port.setPortName(port)
            if serial_port.open(QIODevice.ReadWrite):
                serial_port.setBaudRate(baund)
                serial_port.setRequestToSend(True)
                print(str(port) + " opened.")
            else:
                print(str(port) + " not opened.")
        except IOError:
            print(str(port) + " port already in use.")

    def close_serial_port(self):
        if self.serial_port.isOpen():
            self.serial_port.close()

    def is_open(self):
        return self.serial_port.isOpen()
