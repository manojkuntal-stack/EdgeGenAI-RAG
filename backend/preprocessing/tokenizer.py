import re


def tokenize(text):

    # lowercase
    text = text.lower()

    # keep punctuation useful for chatbot
    text = re.sub(r"([.!?,])", r" \1 ", text)

    # remove unwanted symbols
    text = re.sub(r"[^a-zA-Z0-9.!?,\s]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()

    return tokens


def detokenize(tokens):

    text = " ".join(tokens)

    # fix punctuation spacing
    text = re.sub(r"\s+([.!?,])", r"\1", text)

    return text