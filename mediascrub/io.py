
class TextWriter():
    def __init__(self):
        self.file = None

    def open(self, file_name):
        self.file = open(file_name, "w")

    def write(self, string):
        self.file.write(string)

    def writeLine(self, string):
        self.file.write(string + '\n')

    def close(self):
        self.file.close()