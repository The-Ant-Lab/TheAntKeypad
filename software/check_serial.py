
import os
import sys
import platform
import time
from PySide2.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide2.QtCore import QFile, QIODevice, QByteArray


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


def open_serial_port():
    port = "COM6"
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


if __name__ == "__main__":
    config_os()
    sp = open_serial_port()
    # sp.write("i\n".encode('ascii'))
    sp.write(QByteArray("i\n".encode()))
    sp.waitForBytesWritten(msecs=200)

    time.sleep(0.1)
    sp.write(QByteArray("l\n".encode()))
    sp.waitForBytesWritten(msecs=400)
    c = 0
    while (not sp.waitForReadyRead(msecs=100)) and c < 10:
        c += 1
    data_out = sp.readAll().data()
    print("Max Prog Number: ", int(data_out[0]))
    print("Max Prog Name Len: ", int(data_out[1]))
    print("Keys Number: ", int(data_out[2]))
    print("Chars Number: ", int(data_out[3]))
    print("Led Number: ", int(data_out[4]))

    time.sleep(0.1)
    sp.write(QByteArray("n\n".encode()))
    sp.waitForBytesWritten(msecs=400)
    c = 0
    while (not sp.waitForReadyRead(msecs=100)) and c < 10:
        c += 1
    data_out = sp.readAll().data()
    print("Current Prog Name Len: ", data_out[0])
    print("Current Prog Name: ", data_out[1:-1].decode('ascii'))

    time.sleep(0.1)
    sp.write(QByteArray("n\n".encode()))
    sp.waitForBytesWritten(msecs=400)
    c = 0
    while (not sp.waitForReadyRead(msecs=100)) and c < 10:
        c += 1
    data_out = sp.readAll().data()
    print("Current Prog Name Len: ", data_out[0])
    print("Current Prog Name: ", data_out[1:-1].decode('ascii'))

    time.sleep(0.1)
    sp.write(QByteArray("m\n".encode()))
    sp.waitForBytesWritten(msecs=400)
    sp.write(QByteArray("7\n".encode()))
    sp.waitForBytesWritten(msecs=400)
    c = 0
    while (not sp.waitForReadyRead(msecs=100)) and c < 10:
        c += 1
    data_out = sp.readAll().data()
    print("Name Len: ", int(data_out[0]))

    sp.write(QByteArray("ReSolve\n".encode()))
    sp.waitForBytesWritten(msecs=400)

    sp.write(QByteArray("o\n".encode()))
    sp.waitForBytesWritten(msecs=200)

    sp.close()
