class Log:
    lines = []
    
    def add(self, line):
        self.lines.append(line)
    
    def flush(self):
        for line in self.lines:
            print(line)
        self.lines = []


battle_log = Log()