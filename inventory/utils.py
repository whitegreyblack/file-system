# utils.py

def format_words(word):
    if '\n' in word:
        word = word[:len(word)-1] # removes newlines
    words = word.split('_')
    if len(words) == 1:
        return word
    return ' '.join(word.capitalize() for word in words)

