from enum import Enum
from pathlib import Path
import pickle
import ujson
import uuid


class FreqDictSerializerMode(Enum):
    JSON = ".json"
    PICKLE = ".bin"


class FreqDict:
    """
    Dictionary with letter frequency information.

    Structure: current letter -> previous letters -> next letters -> probability
    """
    def __init__(self, depths, name="", dict={}):
        self.depths = set(depths)
        self.name = name if name else str(uuid.uuid4())
        self._dict = dict

    @property
    def letters(self):
        return list(self._dict.keys())

    def prefixes(self, current):
        """
        Get all strings that can precede this character.
        """
        if current not in self._dict:
            return None
        return self._dict[current]

    def successors(self, current, prefix):
        """
        Get all characters that can come after this character given the previous characters.
        """
        prefixes = self.prefixes(current)
        if prefixes is None:
            return None
        if prefix not in prefixes:
            return None
        return prefixes[prefix]
    
    def freq(self, current, prefix, succ):
        """
        Get the frequency of the character that can come after this character given the previous characters.
        """
        successors = self.successors(current, prefix)
        if successors is None:
            return None
        if succ not in successors:
            return None
        return successors[succ]
    
    def _all_freqs(self):
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
    
    def _all_values(self):
        for letter, prefix, succ in self._all_freqs():
            yield letter, prefix, succ, self.freq(letter, prefix, succ)

    def update(self, current, prefix, next, value=1):
        """
        Update the dict with new data.
        """
        if current not in self._dict:
            self._dict[current] = {}
        
        if prefix not in self.prefixes(current):
            self._dict[current][prefix] = {}
        
        if next not in self.successors(current, prefix):
            self._dict[current][prefix][next] = 1
        
        self._dict[current][prefix][next] += value

    def set(self, current, prefix, next, freq):
        self._dict[current][prefix][next] = freq
    
    def normalize(self):
        """
        Normalize frequencies in the dictionary.
        All values for candidate letters are divided by the highest value.
        """
        for current, prefix, _ in self._all_freqs():
            freqs = self.successors(current, prefix)
            if not freqs:
                continue
            
            freq_sum = sum(freqs.values())
            for letter, value in freqs.items():
                self.set(current, prefix, letter, value / freq_sum)

        return self
    
    def merge(self, other):
        """
        Merge values from the other freqdict into this one.
        """
        self.depths |= other.depths
        for current, prefix, next, freq in other._all_values():
            self.update(current, prefix, next, freq)

        return self
    
    def same_dicts(self, depths):
        return self.depths == set(depths) 
    
    def supports(self, train_depths, gen_depth):
        """
        Does this freqdict support generating with this generation depth and has it been created with these train depths?
        """
        return self.depths.issubset(train_depths) and gen_depth in self.depths


class FreqDictSerializer:
    """
    Class for serializing freqdicts.
    """
    def __init__(self, mode=FreqDictSerializerMode.PICKLE):
        self.mode = mode

    def cache_filename(self, freq_dict):
        return f"{freq_dict.name}"

    def serialize(self, freq_dict):
        """
        Convert a freqdict into a byte stream.
        """
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
    
    def deserialize(self, bytes):
        """
        Convert a byte stream into a freqdict.
        """
        match self.mode:
            case FreqDictSerializerMode.JSON:
                dict = ujson.loads(bytes.decode(encoding="utf-8"))
            case FreqDictSerializerMode.PICKLE:
                dict = pickle.loads(bytes)
            case _:
                raise AttributeError("invalid serializer")
        return FreqDict(depths=set(dict["depths"]), name=dict["name"], dict=dict["freqs"])
