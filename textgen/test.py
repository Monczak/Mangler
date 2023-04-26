from generator.textgen import TextGenerator

textgen = TextGenerator("uploads", "cache")
fd = textgen.analyze("test", [2, 3])
generator = textgen.generate("MACBETH", fd, 3)
print("".join([next(generator) for _ in range(100000)]))
