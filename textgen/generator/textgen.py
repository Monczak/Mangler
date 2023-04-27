import logging
import random

from pathlib import Path
from .freqdict import FreqDict, FreqDictSerializer, FreqDictSerializerMode
from utils.ringbuffer import RingBuffer


class TextgenError(Exception):
    INVALID_DEPTH = 0
    INVALID_SEED = 1

    def __init__(self, kind, message, *args):
        super().__init__(*args)
        self.message = message
        self.kind = kind

    def __str__(self):
        return self.message


class TextGenerator:
    def __init__(self, source_dir, cache_dir, mode=FreqDictSerializerMode.PICKLE):
        self.source_dir = Path(source_dir)
        self.cache_dir = Path(cache_dir)
        self._serializer = FreqDictSerializer(mode)

        if not self.cache_dir.exists():
            self.cache_dir.mkdir()

    def _analyze_text(self, text, depth):
        freq_dict = FreqDict(depths=[depth])

        for i in range(depth, len(text) - 1):
            current = text[i]
            prefix = text[i - depth:i]
            next = text[i + 1]
            freq_dict.update(current, prefix, next)
        
        return freq_dict
    
    def find_files(self, source_id):
        pattern = f"{source_id}.*"
        files = list(Path.glob(self.source_dir, pattern))
        return files

    def analyze(self, source_id, depths):
        files = self.find_files(source_id)
        if not files:
            raise FileNotFoundError(f"No matches for {source_id}")

        logging.info(f"Found {len(files)} source files for {source_id}")

        freq_dict = self.load_cache(source_id)
        if not freq_dict or not freq_dict.same_dicts(depths):
            logging.info(f"Creating new freqdict for {source_id}")
            freq_dict = self.analyze_files(source_id, depths)
            self.save_cache(freq_dict)
        else:
            logging.info(f"Using cached freqdict for {source_id}")

        return freq_dict

    def analyze_files(self, source_id, depths):
        freq_dict = FreqDict(name=source_id, depths=depths)

        for path in self.find_files(source_id):
            with open(path, "r") as text_file:
                text = text_file.read()
                for depth in depths:
                    sub_dict = self._analyze_text(text, depth)
                    freq_dict.merge(sub_dict)
        
        freq_dict.normalize()
        return freq_dict
    
    def save_cache(self, freq_dict):
        logging.info(f"Caching {freq_dict.name}")
        self._serializer.save_cache(freq_dict, self.cache_dir)
    
    def load_cache(self, source_id):
        files = list(Path.glob(self.cache_dir, f"{source_id}.*"))
        if not files:
            return None
        
        found_cache = files[0]
        return FreqDictSerializer.load_cache(found_cache)

    def make_generator(self, seed, freq_dict, depth):
        if depth not in freq_dict.depths:
            raise TextgenError(TextgenError.INVALID_DEPTH, f"Depth {depth} is invalid, must be one of {freq_dict.depths}")
        
        if len(seed) <= depth:
            raise TextgenError(TextgenError.INVALID_SEED, f"Seed \"{seed}\" is too short, must be at least {depth + 1} chars long")
        
        buffer = RingBuffer(depth + 1)
        buffer.fill(seed[-depth - 1:])

        def generator():
            nonlocal buffer
            while True:
                current = buffer.peek()
                previous = "".join(buffer.peek(lookbehind=depth)[:-1])
                candidates = freq_dict.successors(current, previous)

                if not candidates:
                    # Backtrack and try again?
                    pass

                next = random.choices(list(candidates.keys()), weights=list(candidates.values()), k=1)[0]
                buffer.write(next)
                yield next
        
        class GeneratorWrapper:
            def __init__(self, gen):
                self._gen = gen()
                self._count = 0
            
            @property
            def next(self):
                self._count += 1
                return next(self._gen)
            
            @property
            def count(self):
                return self._count

        return GeneratorWrapper(generator)

        