from lib.helper.helper import * 
from datetime import datetime

class Log:

    @classmethod
    def info(cls, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + G + "INFO" + N + "] " + text)

    @classmethod
    def warning(cls, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + Y + "WARNING" + N + "] " + text)

    @classmethod
    def high(cls, text):
        print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + R + "CRITICAL" + N + "] " + text)
