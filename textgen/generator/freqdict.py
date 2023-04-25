class FreqDict:
    def __init__(self):
        self._dict = {}

    @property
    def letters(self):
        return list(self._dict.keys())

    def prefixes(self, current):
        if current not in self._dict:
            return None
        return self._dict[current]

    def successors(self, current, prefix):
        prefixes = self.prefixes(current)
        if prefixes is None:
            return None
        if prefix not in prefixes:
            return None
        return prefixes[prefix]
    
    def freq(self, current, prefix, succ):
        successors = self.successors(current, prefix)
        if successors is None:
            return None
        if succ not in successors:
            return None
        return successors[succ]
    
    def all_freqs(self):
        for letter in self.letters:
            for prefix in self.prefixes(letter):
                for succ in self.successors(letter, prefix):
                    yield letter, prefix, succ
    
    def all_values(self):
        for letter, prefix, succ in self.all_freqs():
            yield letter, prefix, succ, self.freq(letter, prefix, succ)

    def update(self, current, previous, next, value=1):
        if current not in self._dict:
            self._dict[current] = {}
        
        if previous not in self.prefixes(current):
            self._dict[current][previous] = {}
        
        if next not in self.successors(current, previous):
            self._dict[current][previous][next] = 1
        
        self._dict[current][previous][next] += value

    def set(self, current, prefix, next, freq):
        self._dict[current][prefix][next] = freq
    
    def normalize(self):
        for current, prefix, _ in self.all_freqs():
            freqs = self.successors(current, prefix)
            freq_sum = sum(freqs.values())
            for letter, value in freqs.items():
                self.set(current, prefix, letter, value / freq_sum)

        return self
    
    def merge(self, other):
        for current, prefix, next, freq in other.all_values():
            self.update(current, prefix, next, freq)

        return self
