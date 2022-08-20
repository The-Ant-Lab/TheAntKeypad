
class PcKeyboard:

    def __init__(self):
        self.special_keys = {
            "KEY_LEFT_CTRL": "Control",
            "KEY_LEFT_SHIFT": "Shift",
            "KEY_LEFT_ALT": "Alt",
            "KEY_LEFT_GUI": "Meta",
            "KEY_RIGHT_CTRL": "Control",
            "KEY_RIGHT_SHIFT": "Shift",
            "KEY_RIGHT_ALT": "Alt",
            "KEY_RIGHT_GUI": "Meta",
            "KEY_TAB": "Tab",
            "KEY_CAPS_LOCK": "CapsLock",
            "KEY_BACKSPACE": "Backspace",
            "KEY_RETURN": "Return",
            "KEY_MENU": "Menu",
            "KEY_INSERT": "Insert",
            "KEY_DELETE": "Delete",
            "KEY_HOME": "Home",
            "KEY_END": "End",
            "KEY_PAGE_UP": "PageUp",
            "KEY_PAGE_DOWN": "PageDown",
            "KEY_UP_ARROW": "Up",
            "KEY_DOWN_ARROW": "Down",
            "KEY_LEFT_ARROW": "Left",
            "KEY_RIGHT_ARROW": "Right",
            "KEY_NUM_LOCK": "NumLock",
            "KEY_KP_SLASH": "Slash",
            "KEY_KP_ASTERISK": "Asterisk",
            "KEY_KP_MINUS": "Minus",
            "KEY_KP_PLUS": "Plus",
            "KEY_KP_ENTER": "Enter",
            "KEY_KP_1": "1",
            "KEY_KP_2": "2",
            "KEY_KP_3": "3",
            "KEY_KP_4": "4",
            "KEY_KP_5": "5",
            "KEY_KP_6": "6",
            "KEY_KP_7": "7",
            "KEY_KP_8": "8",
            "KEY_KP_9": "9",
            "KEY_KP_0": "0",
            "KEY_KP_DOT": "Period",
            "KEY_ESC": "Escape",
            "KEY_F1": "F1",
            "KEY_F2": "F2",
            "KEY_F3": "F3",
            "KEY_F4": "F4",
            "KEY_F5": "F5",
            "KEY_F6": "F6",
            "KEY_F7": "F7",
            "KEY_F8": "F8",
            "KEY_F9": "F9",
            "KEY_F10": "F10",
            "KEY_F11": "F11",
            "KEY_F12": "F12",
            "KEY_F13": "F13",
            "KEY_F14": "F14",
            "KEY_F15": "F15",
            "KEY_F16": "F16",
            "KEY_F17": "F17",
            "KEY_F18": "F18",
            "KEY_F19": "F19",
            "KEY_F20": "F20",
            "KEY_F21": "F21",
            "KEY_F22": "F22",
            "KEY_F23": "F23",
            "KEY_F24": "F24",
            "KEY_PRINT_SCREEN": "PrintScreen",
            "KEY_SCROLL_LOCK": "ScrollLock",
            "KEY_PAUSE": "Pause",
            "KEY_SPACE": "Any",
            "]": "BracketRight",
            "[": "BracketLeft",
            "}": "BraceRight",
            "{": "BraceLeft",
        }

        self.data = []
        self.index = []

        for k in self.special_keys.keys():
            d = self.special_keys[k]
            self.index.append(d)
            self.data.append(k)

    def get_pc_key(self, ardu_key):
        if ardu_key in self.data:
            id = self.data.index(ardu_key)
            key = self.index[id]
            return key
        else:
            return None

    def get_ardu_key(self, pc_key):
        if pc_key in self.index:
            id = self.index.index(pc_key)
            key = self.data[id]
            return key
        else:
            return None
