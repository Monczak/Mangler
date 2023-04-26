class RingBuffer:
    def __init__(self, size):
        self.size = size
        self._buffer = [None] * size
        self.pos = size - 1
    
    def fill(self, collection):
        if len(collection) != self.size:
            raise ValueError("iterable length and buffer size are not equal")
        
        for i in range(len(collection)):
            self._buffer[i] = collection[i]

    def write(self, item):
        self.pos += 1
        self.pos %= self.size
        self._buffer[self.pos] = item

    def get(self, offset):
        return self._buffer[(self.pos + offset) % self.size]

    def peek(self, lookbehind=0):
        if not 0 <= self.size - 1:
            raise ValueError("lookbehind must be between 0 and buffer size - 1")
        result = [self.get(offset) for offset in range(-lookbehind, 1)]
        return result if lookbehind > 0 else result[0]
    