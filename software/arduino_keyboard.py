# from: https://www.arduino.cc/reference/en/language/functions/usb/keyboard/keyboardmodifiers/

class ArduinoKeyboard:
    
    def __init__(self):
        self.special_keys = {
            "KEY_LEFT_CTRL": (0X80, 128),
            "KEY_LEFT_SHIFT": (0X81, 129),
            "KEY_LEFT_ALT": (0X82, 130),
            "KEY_LEFT_GUI": (0X83, 131),
            "KEY_RIGHT_CTRL": (0X84, 132),
            "KEY_RIGHT_SHIFT": (0X85, 133),
            "KEY_RIGHT_ALT": (0X86, 134),
            "KEY_RIGHT_GUI": (0X87, 135),
            "KEY_TAB": (0XB3, 179),
            "KEY_CAPS_LOCK": (0XC1, 193),
            "KEY_BACKSPACE": (0XB2, 178),
            "KEY_RETURN": (0XB0, 176),
            "KEY_MENU": (0XED, 237),
            "KEY_INSERT": (0XD1, 209),
            "KEY_DELETE": (0XD4, 212),
            "KEY_HOME": (0XD2, 210),
            "KEY_END": (0XD5, 213),
            "KEY_PAGE_UP": (0XD3, 211),
            "KEY_PAGE_DOWN": (0XD6, 214),
            "KEY_UP_ARROW": (0XDA, 218),
            "KEY_DOWN_ARROW": (0XD9, 217),
            "KEY_LEFT_ARROW": (0XD8, 216),
            "KEY_RIGHT_ARROW": (0XD7, 215),
            "KEY_NUM_LOCK": (0XDB, 219),
            "KEY_KP_SLASH": (0XDC, 220),
            "KEY_KP_ASTERISK": (0XDD, 221),
            "KEY_KP_MINUS": (0XDE, 222),
            "KEY_KP_PLUS": (0XDF, 223),
            "KEY_KP_ENTER": (0XE0, 224),
            "KEY_KP_1": (0XE1, 225),
            "KEY_KP_2": (0XE2, 226),
            "KEY_KP_3": (0XE3, 227),
            "KEY_KP_4": (0XE4, 228),
            "KEY_KP_5": (0XE5, 229),
            "KEY_KP_6": (0XE6, 230),
            "KEY_KP_7": (0XE7, 231),
            "KEY_KP_8": (0XE8, 232),
            "KEY_KP_9": (0XE9, 233),
            "KEY_KP_0": (0XEA, 234),
            "KEY_KP_DOT": (0XEB, 235),
            "KEY_ESC": (0XB1, 177),
            "KEY_F1": (0XC2, 194),
            "KEY_F2": (0XC3, 195),
            "KEY_F3": (0XC4, 196),
            "KEY_F4": (0XC5, 197),
            "KEY_F5": (0XC6, 198),
            "KEY_F6": (0XC7, 199),
            "KEY_F7": (0XC8, 200),
            "KEY_F8": (0XC9, 201),
            "KEY_F9": (0XCA, 202),
            "KEY_F10": (0XCB, 203),
            "KEY_F11": (0XCC, 204),
            "KEY_F12": (0XCD, 205),
            "KEY_F13": (0XF0, 240),
            "KEY_F14": (0XF1, 241),
            "KEY_F15": (0XF2, 242),
            "KEY_F16": (0XF3, 243),
            "KEY_F17": (0XF4, 244),
            "KEY_F18": (0XF5, 245),
            "KEY_F19": (0XF6, 246),
            "KEY_F20": (0XF7, 247),
            "KEY_F21": (0XF8, 248),
            "KEY_F22": (0XF9, 249),
            "KEY_F23": (0XFA, 250),
            "KEY_F24": (0XFB, 251),
            "KEY_PRINT_SCREEN": (0XCE, 206),
            "KEY_SCROLL_LOCK": (0XCF, 207),
            "KEY_PAUSE": (0XD0, 208),
            "KEY_SPACE": (0X20, 32),
        }

        self.data = []
        self.index = []

        for k in self.special_keys.keys():
            d = self.special_keys[k]
            self.index.append(d[1])
            self.data.append(k)

    def get_key(self, code):
        if code in self.index:
            id = self.index.index(code)
            key = self.data[id]
            return key
        else:
            return None

    def get_code(self, key):
        if key in self.data:
            id = self.data.index(key)
            code = self.index[id]
            return code
        else:
            return None