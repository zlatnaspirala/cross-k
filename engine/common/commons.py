import re

def crossKvalidateNumbers(txt):
    return re.findall('[^0-9]', txt)
