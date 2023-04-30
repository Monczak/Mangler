import logging
import random

from pathlib import Path
from .freqdict import FreqDict
from utils.ringbuffer import RingBuffer


logger = logging.getLogger("mangler")


class TextgenError(Exception):
    def __init__(self, message=None, *args):
        super().__init__(*args)
        self.message = message

    def __str__(self):
        return self.message
    

class DepthError(TextgenError):
    pass


class SeedError(TextgenError):
    pass


class StuckError(TextgenError):
    def __init__(self, message=None, current=None, previous=None, *args):
        super().__init__(message, *args)
        self.current = current
        self.previous = previous


class TextGenerator:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)

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

        logger.info(f"Found {len(files)} source files for {source_id}")

        freq_dict = self.analyze_files(source_id, depths)
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

    def make_generator(self, seed, freq_dict, depth):
        if depth not in freq_dict.depths:
            raise DepthError(f"Depth {depth} is invalid, must be one of {freq_dict.depths}")
        
        if len(seed) <= depth:
            raise SeedError(f"Seed \"{seed}\" is too short, must be at least {depth + 1} chars long")
        
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
                    raise StuckError(current=current, previous=previous)

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

        