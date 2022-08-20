
import time
import serial

ser = serial.Serial('COM5', 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=1)

flag = True
prog_name_len = -1

print("Prog Num:")
ser.write("p\n")
data = ser.read(1)
try:
    print(ord(data))
except:
    flag = False
    ser.close()

if flag:
    print("Setup:")
    ser.write("l\n")
    data = ser.read(5)
    max_progs_num = ord(data[0])
    prog_name_len = ord(data[1])
    keys_number = ord(data[2])
    key_seq_len = ord(data[3])
    leds_number = ord(data[4])
    try:
        print("Max Progs Number: " + str(max_progs_num))
        print("Prog Name Len: " + str(prog_name_len))
        print("Number of Keys: " + str(keys_number))
        print("Key Sequence Len: " + str(key_seq_len))
        print("LEDs Number: " + str(leds_number))
    except:
        flag = False
        ser.close()

if flag:
    print("Prog Name:")
    ser.write("n\n")
    this_prog_name_len = ord(ser.read(1));
    data = ser.read(this_prog_name_len)
    try:
        print(data)
    except:
        flag = False
        ser.close()

if flag:
    print("Active Prog:")
    ser.write("c\n")
    data = ser.read(1)
    try:
        print(ord(data))
    except:
        flag = False
        ser.close()

if flag and False:
    print("Set Active Prog to")
    ser.write("h\n")
    ser.write("2\n")
    ser.write("c\n")
    data = ser.read(1)
    try:
        print(ord(data))
    except:
        flag = False
        ser.close()

if flag:
    print("Change Prog Name in:")
    ser.write("m\n")
    ser.write("9\n")
    a = ser.read(1)
    print("Recived: " + str(ord(a)))
    ser.write(b'LudipipoM' + "\n")
    time.sleep(1)
    print("New Name:")
    ser.write("n\n")
    try:
        this_prog_name_len = ord(ser.read(1));
        data = ser.read(this_prog_name_len)
        print(data)
    except:
        flag = False
        ser.close()
        
if flag:
    print("Read Prog String:")
    ser.write("s\n")
    data = ser.read(keys_number*key_seq_len)
    print("Len Data: " + str(len(data)))
    try:
        for i in range(len(data)):
            if data[i].isalpha():
                print(data[i])
            else:
                print(ord(data[i]))
    except:
        flag = False
        ser.close()

if flag:
    print("Mod Keys")
    ser.write("k\n")
    ser.write("0\n")
    ser.write("6\n")
    ser.write(b'\x6d\x61\x00\x74\x74\x00')
    ser.write("\n")
    print(ser.read(6))

ser.close()
