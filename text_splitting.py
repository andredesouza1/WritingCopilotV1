import re

def split_text(text):
    sentences = [sentence for sentence in re.split('[.!?]', text) if sentence.strip()]
    return sentences