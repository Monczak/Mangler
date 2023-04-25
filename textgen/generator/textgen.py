from pathlib import Path
from freqdict import FreqDict


class TextGenerator:
    def __init__(self, source_dir, output_dir, cache_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.cache_dir = Path(cache_dir)

    def _analyze_text(self, text, depth):
        freq_dict = FreqDict()

        for i in range(depth, len(text) - 1):
            current = text[i]
            prefix = text[i - depth:i]
            next = text[i + 1]
            freq_dict.update(current, prefix, next)
        
        return freq_dict
            

    def analyze(self, source_id, depths):
        pattern = f"{source_id}.*"       
        freq_dict = FreqDict()

        for file in Path.glob(self.source_dir, pattern):
            with open(file, "r") as text_file:
                text = text_file.read()
                for depth in depths:
                    sub_dict = self._analyze_text(text, depth)
                    freq_dict.merge(sub_dict)
        
        return freq_dict
    
    def generate(self):
        raise NotImplementedError()
            
        