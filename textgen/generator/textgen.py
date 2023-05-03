import logging
import random

from dataclasses import dataclass, asdict

from pathlib import Path
from .freqdict import FreqDict
from utils.ringbuffer import RingBuffer
from utils.generator_utils import GeneratorWrapper, keep_value


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


class SeedLengthError(SeedError):
    pass


class BadSeedError(SeedError):
    pass


class StuckError(TextgenError):
    def __init__(self, message=None, current=None, previous=None, *args):
        super().__init__(message, *args)
        self.current = current
        self.previous = previous


@dataclass
class AnalysisProgress:
    file_current: int
    file_total: int
    text_current: int
    text_total: int

    def dict(self):
        return asdict(self)


class TextGenerator:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)

    @keep_value
    def _make_text_analyzer(self, text, depth):
        freq_dict = FreqDict(depths=[depth])

        for i in range(depth, len(text) - 1):
            current = text[i]
            prefix = text[i - depth:i]
            next = text[i + 1]
            freq_dict.update(current, prefix, next)
            yield i, len(text)

        # Wrap around at the end of the text
        freq_dict.update(current=text[-1], prefix=text[-depth-1:-1], next=text[0])
        
        return freq_dict
    
    def find_files(self, source_id):
        """
        Find files in the source directory that match the specified ID.
        """
        pattern = f"{source_id}.*"
        files = list(Path.glob(self.source_dir, pattern))
        return files

    @keep_value
    def make_analyzer(self, source_id, depths):
        """
        Analyze files in the source directory that match the specified ID and return a normalized dictionary of letter sequence frequencies.
        Also check if files are present and valid.
        Yield progress information and return the freqdict.
        """
        files = self.find_files(source_id)
        if not files:
            raise FileNotFoundError(f"No matches for {source_id}")

        logger.info(f"Found {len(files)} source files for {source_id}")

        analyzer = self.make_file_analyzer(source_id, depths)
        for progress_info in analyzer:
            yield progress_info

        freq_dict = analyzer.value
        return freq_dict

    def analyze(self, source_id, depths):
        """
        Analyze files in the source directory that match the specified ID and return a normalized dictionary of letter sequence frequencies.
        Also check if files are present and valid.
        Ignore progress information.
        """
        analyzer = self.make_analyzer(source_id, depths)
        for _ in analyzer:
            pass
        return analyzer.value

    @keep_value
    def make_file_analyzer(self, source_id, depths):
        """
        Analyze files in the source directory that match the specified ID and return a normalized dictionary of letter sequence frequencies.
        """
        freq_dict = FreqDict(name=source_id, depths=depths)

        files = self.find_files(source_id)
        for i in range(len(files)):
            path = files[i]
            with open(path, "r") as text_file:
                text = text_file.read()
                for depth in depths:
                    analyzer = self._make_text_analyzer(text, depth)
                    for current, total in analyzer:
                        yield AnalysisProgress(i, len(files), current, total)
                    sub_dict = analyzer.value
                    freq_dict.merge(sub_dict)
        
        freq_dict.normalize()
        return freq_dict

    def make_generator(self, seed, freq_dict, depth):
        """
        Create a text generator from a frequency dictionary.
        """
        if depth not in freq_dict.depths:
            raise DepthError(f"Depth {depth} is invalid, must be one of {freq_dict.depths}")
        
        if len(seed) <= depth:
            raise SeedLengthError(f"Seed \"{seed}\" is too short, must be at least {depth + 1} chars long")
        
        if not freq_dict.successors(seed[-1], seed[-depth-1:-1]):
            raise BadSeedError(f"Cannot start generation with seed \"{seed}\", no successors found")
        
        buffer = RingBuffer(depth + 1)
        buffer.fill(seed[-depth - 1:])

        def generator():
            nonlocal buffer
            while True:
                current = buffer.peek()
                previous = "".join(buffer.peek(lookbehind=depth)[:-1])
                candidates = freq_dict.successors(current, previous)

                if not candidates:
                    raise StuckError(current=current, previous=previous)

                next = random.choices(list(candidates.keys()), weights=list(candidates.values()), k=1)[0]
                buffer.write(next)
                yield next

        return GeneratorWrapper(generator())

        