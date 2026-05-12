from collections import defaultdict
import random

class NGramModel:

    def __init__(self, n=2):
        self.n = n
        self.model = defaultdict(list)

    def train(self, text):

        tokens = text.split()

        for i in range(len(tokens) - self.n):

            key = tuple(tokens[i:i+self.n-1])

            next_word = tokens[i+self.n-1]

            self.model[key].append(next_word)

    def predict(self, context):

        context = tuple(context)

        if context in self.model:

            return random.choice(self.model[context])

        return ""