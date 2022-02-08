class Measurement:
    def __init__(self, _id, _value, _time, _signal, _sample):
        self.id = _id
        self.value = _value
        self.time = _time
        self.signal = _signal
        self.sample = _sample

    def getId(self):
        return self.id

    def getValue(self):
        return self.value


    def getTime(self):
        return self.time


    def getSignal(self):
        return self.signal

    def getSample(self):
        return self.sample

    def setId(self, id):
        self.id = id

    def setValue(self, value):
        self.value = value


    def setTime(self, time):
        self.time = time


    def setSignal(self, signal):
        self.signal = signal

    def setSample(self, sample):
            self.sample = sample

