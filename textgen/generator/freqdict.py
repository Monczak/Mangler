from enum import Enum
from pathlib import Path
import pickle
import ujson
import uuid


class FreqDictSerializer(Enum):
    JSON = ".json"
    PICKLE = ".bin"


class FreqDict:
    def __init__(self, depths, name="", dict={}, serializer=FreqDictSerializer.PICKLE):
        self.depths = set(depths)
        self.name = name if name else str(uuid.uuid4())
        self._dict = dict
        self._serializer = serializer

    @property
    def letters(self):
        return list(self._dict.keys())
    
    @property
    def cache_filename(self):
        return f"{self.name}{self._serializer.value}"

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
        self.depths |= other.depths
        for current, prefix, next, freq in other.all_values():
            self.update(current, prefix, next, freq)

        return self
    
    def serialize(self):
        dict = {
            "name": self.name,
            "freqs": self._dict,
            "depths": list(self.depths)
        }
        match self._serializer:
            case FreqDictSerializer.JSON:
                return bytes(ujson.dumps(dict), encoding="utf-8")
            case FreqDictSerializer.PICKLE:
                return pickle.dumps(dict)
            case _:
                raise AttributeError("invalid serializer")
    
    @staticmethod
    def deserialize(bytes, serializer):
        match serializer:
            case FreqDictSerializer.JSON:
                dict = ujson.loads(bytes.decode(encoding="utf-8"))
            case FreqDictSerializer.PICKLE:
                dict = pickle.loads(bytes)
            case _:
                raise AttributeError("invalid serializer")
        return FreqDict(depths=set(dict["depths"]), name=dict["name"], dict=dict["freqs"])
    
    def save_cache(self, dir):
        with open(Path(dir) / self.cache_filename, "wb") as file:
            file.write(self.serialize())

    @staticmethod
    def load_cache(path):
        cache_path = Path(path)
        if not cache_path.exists():
            return None
        with open(cache_path, "rb") as file:
            freq_dict = FreqDict.deserialize(file.read(), FreqDictSerializer(cache_path.suffix))
            return freq_dict

    
    def same_dicts(self, depths):
        return self.depths == set(depths) 
