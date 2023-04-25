import logging

from pathlib import Path
from freqdict import FreqDict, FreqDictSerializer


class TextGenerator:
    def __init__(self, source_dir, cache_dir, serializer=FreqDictSerializer.PICKLE):
        self.source_dir = Path(source_dir)
        self.cache_dir = Path(cache_dir)
        self._serializer = serializer

        if not self.cache_dir.exists():
            self.cache_dir.mkdir()

    def _analyze_text(self, text, depth):
        freq_dict = FreqDict(depths=[depth], serializer=self._serializer)

        for i in range(depth, len(text) - 1):
            current = text[i]
            prefix = text[i - depth:i]
            next = text[i + 1]
            freq_dict.update(current, prefix, next)
        
        return freq_dict

    # TODO: Refactor this to separate cache handling 
    def analyze(self, source_id, depths):
        pattern = f"{source_id}.*"

        freq_dict = self.load_cache(source_id)
        if not freq_dict or not freq_dict.same_dicts(depths):
            logging.info(f"Creating new freqdict for {source_id}")
            freq_dict = FreqDict(name=source_id, depths=depths, serializer=self._serializer)

            for file in Path.glob(self.source_dir, pattern):
                with open(file, "r") as text_file:
                    text = text_file.read()
                    for depth in depths:
                        sub_dict = self._analyze_text(text, depth)
                        freq_dict.merge(sub_dict)
            freq_dict.normalize()
            self.save_cache(freq_dict)
        else:
            logging.info(f"Using cached freqdict for {source_id}")

        return freq_dict
    
    def save_cache(self, freq_dict):
        logging.info(f"Caching {freq_dict.name}")
        freq_dict.save_cache(self.cache_dir)
    
    def load_cache(self, source_id):
        files = list(Path.glob(self.cache_dir, f"{source_id}.*"))
        if not files:
            return None
        
        found_cache = files[0]
        return FreqDict.load_cache(found_cache)

    def generate(self):
        raise NotImplementedError()
            
        