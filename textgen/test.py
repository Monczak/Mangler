from generator.textgen import TextGenerator

textgen = TextGenerator("uploads")

fd = textgen.analyze("test", [1])
generator = textgen.make_generator("MACBETH", fd, 3)
print("".join([next(generator) for _ in range(100000)]))
