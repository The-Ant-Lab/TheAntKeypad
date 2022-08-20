import os
import sys
import time
import platform
from collections import OrderedDict as od
from PySide2.QtCore import QIODevice, QByteArray
from PySide2.QtSerialPort import QSerialPort
from arduino_keyboard import ArduinoKeyboard


class KeypadSetup:

    def __init__(self, data_out):
        self.max_prog_number = int(data_out[0])
        self.max_prog_name_len = int(data_out[1])
        self.key_number = int(data_out[2])
        self.key_chars_number = int(data_out[3])
        self.led_number = int(data_out[4])


class TheAntKeypad:

    BAUND_RATE = 115200
    PROG_OFF = 'o'
    PROG_ON = 'i'
    GET_PROG_STATE = 'x'
    GET_SETUP = 'l'
    GET_ACTIVE_PROG_KEYS = 's'
    GET_PROG_NUM = 'p'
    SET_PROG_NUM = 'y'
    GET_CURRENT_PROG = 'c'
    SET_CURRENT_PROG = 'h'
    GET_PROG_NAME = 'n'
    SET_PROG_NAME = 'm'
    SET_PROG_KEYS = 'k'
    SERIAL_WRITE_PROG_ON_EEPROM = 'w'
    SERIAL_LOAD_PROG_FROM_EEPROM = 'd'

    WAIT_WRITTEN_MS = 300
    WAIT_RECEIVED_MS = 300

    def __init__(self, serial_port):
        self.s = serial_port
        self.setup = None
        self.prog_number = -1
        self.ardu_keys = ArduinoKeyboard()
        self.progs_keys = od({})

    def send_command(self, command):
        cmd = command + "\n"
        self.s.write(QByteArray(cmd.encode()))
        self.s.waitForBytesWritten(msecs=self.WAIT_WRITTEN_MS)

    def send_data(self, data):
        cmd = data
        self.s.write(QByteArray(cmd))
        self.s.write(QByteArray("\n".encode()))
        self.s.waitForBytesWritten(msecs=self.WAIT_WRITTEN_MS)

    def get_data(self):
        c = 0
        d = []
        found_flag = False
        print("Receiving:", end="")
        while c < 20 and not found_flag:
            self.wait_data_ready()
            r = self.s.readAll().data()
            if len(r) > 0:
                found_flag = chr(r[-1]) == "\n"
            d.append(r)
            c += 1
            print(c, end=" ")
        print("")
        data = b''.join(d)
        return data.strip()

    def wait_data_ready(self):
        c = 0
        while (not self.s.waitForReadyRead(msecs=self.WAIT_RECEIVED_MS)) and c < 10:
            c += 1
        return False if c >= 10 else True

    def activate_programming(self):
        self.send_command(self.PROG_ON)

    def deactivate_programming(self):
        self.send_command(self.PROG_OFF)

    def get_setup(self):
        time.sleep(0.1)
        self.send_command(self.GET_SETUP)
        data_out = self.get_data()
        self.setup = KeypadSetup(data_out)

    def get_prog_number(self):
        self.send_command(self.GET_PROG_NUM)
        data = self.get_data()
        self.prog_number = int(data[0])
        return self.prog_number

    def set_active_prog(self, id):
        if self.prog_number > 0:
            if id < self.prog_number:
                self.send_command(self.SET_CURRENT_PROG)
                self.send_command(str(id))

    def get_active_prog_name(self):
        self.send_command(self.GET_PROG_NAME)
        data = self.get_data()
        print(str(data[1:].decode(errors='replace')))
        return str(data[1:].decode(errors='replace'))

    def set_active_prog_keys(self, keys_l):
        k_n = self.setup.key_number
        c_n = self.setup.key_chars_number
        for j, k in enumerate(keys_l):
            if j < k_n:
                seq_len = len(k)
                data = self.get_keys_code(k)
                if seq_len > c_n:
                    data = data[0:c_n]
                self.send_command(self.SET_PROG_KEYS)
                self.send_command(str(j))
                self.send_data(data)
                time.sleep(0.1)

    def get_keys_code(self, kl):
        a = bytearray(b'')
        for k in kl:
            c = self.ardu_keys.get_code(k)
            if c is not None:
                a.append(c)
            else:
                if isinstance(k, str):
                    kd = bytes(k.lower(), 'utf-8')
                    if len(kd) > 0:
                        a.append(kd[0])
                    else:
                        a.append(0)
                else:
                    a.append(k)
        return a

    def get_active_prog_keys(self):
        keys = []
        if self.setup is not None:
            k_n = self.setup.key_number
            c_n = self.setup.key_chars_number
            self.send_command(self.GET_ACTIVE_PROG_KEYS)
            data = self.get_data()
            c = 0
            while len(data) < 1 and c < 10:
                data = self.get_data()
                c += 1
            if c < 10 and k_n * c_n <= len(data):
                for i in range(k_n):
                    chars = []
                    for j in range(c_n):
                        c = data[i*c_n + j]
                        if c != 0:
                            ak = self.ardu_keys.get_key(c)
                            if ak is not None:
                                chars.append(str(ak))
                            else:
                                chars.append(chr(c))
                    keys.append(tuple(chars))
            else:
                print("ERROR incorrect program keys data")
        return keys

    def get_progs_keys(self):
        progs_keys = od({})
        if self.setup is not None:
            if self.prog_number > 0:
                for i in range(self.prog_number):
                    self.set_active_prog(i)
                    name = self.get_active_prog_name()
                    name = name.replace("\x00", "", -1)
                    keys = self.get_active_prog_keys()
                    progs_keys[name] = keys
        self.progs_keys = progs_keys
        return progs_keys

    def get_dummy_values(self):
        data_out = ["5", "9", "11", "3", "8"]
        self.setup = KeypadSetup(data_out)
        self.prog_number = 3
        data = od({
            'Eagle': [('KEY_LEFT_CTRL', 'm'), ('KEY_LEFT_CTRL', 'r'), ('KEY_LEFT_CTRL', 'KEY_LEFT_SHIFT', 'x'),
                      ('KEY_LEFT_CTRL', 'KEY_LEFT_SHIFT', 'm'), ('KEY_LEFT_CTRL', 'KEY_LEFT_SHIFT', 'r'),
                      ('KEY_LEFT_CTRL', 'KEY_LEFT_SHIFT', 'a'), ('KEY_LEFT_CTRL', 'G'), ('KEY_ESC',), ('k',), ('+',),
                      ('-',)],
            'DaVinci': [('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',), ('H',), ('I',), ('+',), ('-',)],
            'OBS': [('a',), ('b',), ('c',), ('d',), ('e',), ('f',), ('g',), ('h',), ('i',), ('+',), ('-',)]
        })
        return data

    def write_on_eeprom(self):
        if self.setup is not None:
            self.send_command(self.SERIAL_WRITE_PROG_ON_EEPROM)


if __name__ == "__main__":

    port = "COM6"

    def open_serial_port(port):
        serial_port = QSerialPort()
        try:
            serial_port.setPortName(port)
            if serial_port.open(QIODevice.ReadWrite):
                serial_port.setBaudRate(115200)
                serial_port.setRequestToSend(True)
                print(str(port) + " opened.")
            else:
                print(str(port) + " not opened.")
        except IOError:
            print(str(port) + " port already in use.")
        return serial_port

    def config_os():
        pys2_path = os.path.dirname(sys.modules['PySide2'].__file__)
        if os.path.isdir(os.path.join(pys2_path, "Qt")):
            pys2_path = os.path.join(pys2_path, "Qt")

        # Simple mod to set the QT environment data just for python
        # avoiding conflict with other applications using Qt
        os.environ["QT_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins")

        sys_name = platform.system()
        print(sys_name)
        if sys_name == "Windows":
            print("Windows Env")
        elif sys_name == 'Darwin':
            print("Mac Env")
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
        else:
            print("Linux Env")
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pys2_path, "plugins", "platforms")
            os.environ["QT_QPA_PLATFORM"] = "xcb"

    config_os()
    s = open_serial_port(port)

    kp = TheAntKeypad(s)
    dummy = False
    if dummy:
        data = kp.get_dummy_values()
    else:
        kp.activate_programming()
        kp.get_setup()
        kp.get_prog_number()
        data = kp.get_progs_keys()
        kp.deactivate_programming()
    print(data)
