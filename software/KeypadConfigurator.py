import os
import sys
import platform
from collections import OrderedDict as od

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import resources
from configurator_gui import Ui_MainWindow
from serial_interface import SerialInterface
from theant_keypad import TheAntKeypad
from pc_keyboard import PcKeyboard


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


class DetectorTextEdit(QTextEdit):
    def __init__(self, key_parent):
        super(DetectorTextEdit, self).__init__()
        self.key_pressed_list = []
        self.key_list = []
        self.grab_on = False
        self.state = 0
        self.key_parent = key_parent
        self.last_string = ""

    def event(self, event):
        if self.grab_on:
            if (event.type() == QtCore.QEvent.KeyPress) and\
                    (event.key() == QtCore.Qt.Key_Tab
                     or event.key() == QtCore.Qt.Key_Backtab
                     or event.key() == QtCore.Qt.Key_Menu):
                last_string = self.keyevent_to_string(event)
                self.setPlainText(last_string)
                return True
        return QTextEdit.event(self, event)

    def keyPressEvent(self, event):
        if self.grab_on:
            self.state = 1
            if event.key() not in self.key_list:
                self.key_list.append(event.key())
                last_string = self.keyevent_to_string(event)
                self.setPlainText(last_string)
                if event.key() not in self.key_pressed_list:
                    self.key_pressed_list.append(event.key())
        else:
            self.state = 0
            self.key_list = []
            self.key_pressed_list = []
        event.accept()

    def keyReleaseEvent(self, event):
        if event.key() in self.key_pressed_list:
            self.key_pressed_list.remove(event.key())
        if not self.key_pressed_list and self.state == 1:
            self.key_list = []
            self.grab_on = False
            self.state = 0
        event.accept()

    def keyevent_to_string(self, event):
        sequence = []
        for modifier, text in self.key_parent.modmap.items():
            if event.modifiers() & modifier:
                sequence.append(text)
        key = self.key_parent.keymap.get(event.key(), event.text().lower())
        if len(key) == 1:
            key = key.lower()
        if key not in sequence:
            sequence.append(key)
        return " + ".join(sequence)


class KeyItem:
    def __init__(self, name, default, parent, keymap, modmap):
        self.parent = parent
        self.default = default
        self.name = name
        self.widgets = []
        self.grab_button = None
        self.grab_line = None
        self.default_button = None
        self.layout = None
        self.keymap = keymap
        self.modmap = modmap

    def create_widgets(self):
        # print("create " + str(self.name) + " " + str(self.default))
        grab_button = QPushButton(self.name)
        grab_button.setMinimumSize(100, 30)
        grab_button.setMaximumSize(100, 30)
        grab_button.clicked.connect(self.on_grab)
        grab_line = DetectorTextEdit(self)
        grab_line.setReadOnly(True)
        grab_line.setMinimumHeight(30)
        grab_line.setMaximumHeight(30)
        grab_txt = " + ".join(self.default)
        grab_line.setPlainText(grab_txt)
        default_button = QPushButton("Default")
        default_button.setMinimumSize(100, 30)
        default_button.setMaximumSize(100, 30)
        default_button.clicked.connect(self.on_default)

        hl = QHBoxLayout()
        hl.addWidget(grab_button)
        hl.addWidget(grab_line)
        hl.addWidget(default_button)

        self.grab_button = grab_button
        self.grab_line = grab_line
        self.default_button = default_button
        self.layout = hl
        self.parent.addLayout(hl)

        self.widgets = []
        self.widgets.append(grab_button)
        self.widgets.append(grab_line)
        self.widgets.append(default_button)
        self.widgets.append(hl)

    def on_default(self):
        grab_txt = " + ".join(self.default)
        self.grab_line.setPlainText(grab_txt)

    def destroy_widgets(self):
        # print("destroy " + str(self.name) + " " + str(self.default))
        for w in self.widgets:
            w.deleteLater()

    def on_grab(self):
        # print("Grab Keys Sequence")
        self.grab_line.grab_on = True
        self.grab_line.setFocus()

    def get_keys_sequence(self):
        txt = self.grab_line.toPlainText()
        ks = [x.strip() for x in txt.split("+")]
        return ks


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        appIcon = QtGui.QIcon(":/images/keypad_icon.png")
        self.setWindowIcon(appIcon)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        sshFile = "darkorange.stylesheet"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())
        self.ui.connection_lb.setStyleSheet("color: white; font-weight: bold;"
                                            "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.serial = SerialInterface()
        self.keypad = None
        self.progs_keys = od({})

        self.keymap = {}
        self.modmap = {}
        self.pc_keyboard_map = PcKeyboard()

        # Serial Section
        self.ui.refresh_bt.clicked.connect(self.on_refresh)
        self.ui.connection_bt.clicked.connect(self.on_connect)
        self.ui.coms_cb.currentIndexChanged.connect(self.on_com_changed)

        # Programs Section
        self.scroll_region_widget = []
        self.ui.load_progs_bt.clicked.connect(self.on_load_progs)
        self.ui.progs_cb.currentIndexChanged.connect(self.on_progs_change)
        self.ui.update_bt.clicked.connect(self.on_update)
        self.ui.write_bt.clicked.connect(self.on_write)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.ui.scrollArea.setWidget(self.scroll_widget)
        self.load_keys_name()

    def on_write(self):
        if self.keypad is not None:
            self.keypad.activate_programming()
            self.keypad.write_on_eeprom()
            self.keypad.deactivate_programming()

    def on_update(self):
        prog_name = self.ui.progs_cb.currentText()
        keys_sequences = []
        for w in self.scroll_region_widget:
            ks = w.get_keys_sequence()
            aks = self.get_arduino_keys_sequence(ks)
            keys_sequences.append(aks)
        if prog_name in self.progs_keys:
            self.progs_keys[prog_name] = keys_sequences
            self.update_keypad_prog(prog_name)

    def update_keypad_prog(self, prog_name):
        progs_l = list(self.progs_keys.keys())
        if prog_name in progs_l:
            id = progs_l.index(prog_name)
            if self.keypad is not None:
                self.keypad.activate_programming()
                prog_num = self.keypad.get_prog_number()
                if id < prog_num:
                    self.keypad.set_active_prog(id)
                    self.keypad.set_active_prog_keys(self.progs_keys[prog_name])
                self.keypad.deactivate_programming()

    def load_keys_name(self):
        keymap = {}
        for key, value in vars(QtCore.Qt).items():
            if isinstance(value, QtCore.Qt.Key):
                keymap[value] = key.partition('_')[2]
        modmap = {
            QtCore.Qt.ControlModifier: keymap[QtCore.Qt.Key_Control],
            QtCore.Qt.AltModifier: keymap[QtCore.Qt.Key_Alt],
            QtCore.Qt.ShiftModifier: keymap[QtCore.Qt.Key_Shift],
            QtCore.Qt.MetaModifier: keymap[QtCore.Qt.Key_Meta],
            QtCore.Qt.GroupSwitchModifier: keymap[QtCore.Qt.Key_AltGr],
            QtCore.Qt.KeypadModifier: keymap[QtCore.Qt.Key_NumLock],
        }
        self.keymap = keymap
        self.modmap = modmap

    def on_progs_change(self):
        if self.progs_keys:
            self.update_scroll_region()

    def on_load_progs(self):
        if self.serial.is_open():
            self.keypad = TheAntKeypad(self.serial.serial_port)
            self.keypad.activate_programming()
            self.keypad.get_setup()
            self.keypad.get_prog_number()
            data = self.keypad.get_progs_keys()
            self.keypad.deactivate_programming()
            if data:
                progs_name = list(data.keys())
                self.ui.progs_cb.clear()
                self.ui.progs_cb.addItems(progs_name)
                self.progs_keys = data
                self.update_scroll_region()

    def update_scroll_region(self):
        for w in self.scroll_region_widget:
            w.destroy_widgets()
        self.scroll_region_widget = []

        prog = self.ui.progs_cb.currentText()
        if prog in self.progs_keys.keys():
            data = self.progs_keys[prog]
            for i, d in enumerate(data):
                default_seq = self.get_default_pc_seq(d)
                w = KeyItem("KEY" + str(i+1), default_seq, self.scroll_layout, self.keymap, self.modmap)
                w.create_widgets()
                self.scroll_region_widget.append(w)

    def get_default_pc_seq(self, dl):
        pc_def = []
        for d in dl:
            c = self.pc_keyboard_map.get_pc_key(d)
            if c is not None:
                pc_def.append(c)
            else:
                pc_def.append(d)
        return pc_def

    def get_arduino_keys_sequence(self, ks):
        ardu_sequence = []
        for k in ks:
            c = self.pc_keyboard_map.get_ardu_key(k)
            if c is not None:
                ardu_sequence.append(c)
            else:
                ardu_sequence.append(k)
        return ardu_sequence

    def on_com_changed(self):
        port = self.ui.coms_cb.currentText()
        baund = self.ui.baund_rate_cb.currentText()
        if port:
            self.serial.load_baund_rate_from_port(port)
            baund_str_l = [str(x) for x in self.serial.bauds_l]
            baund_str = str(self.serial.get_default_baund_rate())
            if baund in baund_str_l:
                baund_str = baund
            self.ui.baund_rate_cb.clear()
            self.ui.baund_rate_cb.addItems(baund_str_l)
            self.ui.baund_rate_cb.setCurrentText(baund_str)

    def on_connect(self):
        self.serial.close_serial_port()
        port = self.ui.coms_cb.currentText()
        baund = int(self.ui.baund_rate_cb.currentText())
        self.serial.open_serial_port(port, baund)
        if port and baund:
            if self.serial.is_open():
                self.ui.connection_lb.setStyleSheet("color: black; font-weight: bold;"
                    "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);")
                self.ui.connection_lb.setText("Connected")
            else:
                self.ui.connection_lb.setStyleSheet("color: white; font-weight: bold;"
                    "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);")
                self.ui.connection_lb.setText("Not Connected")

    def on_refresh(self):
        self.serial.refresh_com_list()
        self.ui.coms_cb.clear()
        self.ui.coms_cb.addItems(self.serial.port_name_l)
        self.ui.baund_rate_cb.clear()
        self.ui.baund_rate_cb.addItems([str(x) for x in self.serial.bauds_l])
        self.ui.baund_rate_cb.setCurrentText(str(self.serial.get_default_baund_rate()))


if __name__ == "__main__":
    config_os()

    app = QApplication(sys.argv)
    # app.setStyle("plastique")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
