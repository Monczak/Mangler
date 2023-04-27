from enum import Enum
from pathlib import Path
import pickle
import ujson
import uuid


class FreqDictSerializerMode(Enum):
    JSON = ".json"
    PICKLE = ".bin"


class FreqDict:
    def __init__(self, depths, name="", dict={}):
        self.depths = set(depths)
        self.name = name if name else str(uuid.uuid4())
        self._dict = dict

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
            prefixes = self.prefixes(letter)
            if not prefixes: 
                continue

            for prefix in prefixes:
                successors = self.successors(letter, prefix)
                if not successors:
                    continue

                for succ in successors:
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
            if not freqs:
                continue
            
            freq_sum = sum(freqs.values())
            for letter, value in freqs.items():
                self.set(current, prefix, letter, value / freq_sum)

        return self
    
    def merge(self, other):
        self.depths |= other.depths
        for current, prefix, next, freq in other.all_values():
            self.update(current, prefix, next, freq)

        return self
    
    def same_dicts(self, depths):
        return self.depths == set(depths) 
    
    def supports(self, train_depths, gen_depth):
        return self.depths.issubset(train_depths) and gen_depth in self.depths


class FreqDictSerializer:
    def __init__(self, mode):
        self.mode = mode

    def cache_filename(self, freq_dict):
        return f"{freq_dict.name}{self.mode.value}"

    def serialize(self, freq_dict):
        dict = {
            "name": freq_dict.name,
            "freqs": freq_dict._dict,
            "depths": list(freq_dict.depths)
        }
        match self.mode:
            case FreqDictSerializerMode.JSON:
                return bytes(ujson.dumps(dict), encoding="utf-8")
            case FreqDictSerializerMode.PICKLE:
                return pickle.dumps(dict)
            case _:
                raise AttributeError("invalid serializer")
    
    @staticmethod
    def deserialize(bytes, serializer):
        match serializer:
            case FreqDictSerializerMode.JSON:
                dict = ujson.loads(bytes.decode(encoding="utf-8"))
            case FreqDictSerializerMode.PICKLE:
                dict = pickle.loads(bytes)
            case _:
                raise AttributeError("invalid serializer")
        return FreqDict(depths=set(dict["depths"]), name=dict["name"], dict=dict["freqs"])
    
    def save_cache(self, freq_dict, dir):
        with open(Path(dir) / self.cache_filename(freq_dict), "wb") as file:
            file.write(self.serialize(freq_dict))        

    @staticmethod
    def load_cache(path):
        cache_path = Path(path)
        if not cache_path.exists():
            return None
        with open(cache_path, "rb") as file:
            freq_dict = FreqDictSerializer.deserialize(file.read(), FreqDictSerializerMode(cache_path.suffix))
            return freq_dict
