from cs50 import get_string


letters = 0 # total number of words in string
sentences = 0 # total number of sentences in string
words = 1

frase = get_string("Text: ")

for i in range(0, len(frase)):
    if frase[i] == '.' or frase[i] == '!' or frase[i] == '?':
        sentences += 1
    if frase[i].isalnum():
        letters += 1
    if frase[i] == ' ':
        words += 1

L = int((letters * 100.0) / words) # average number of letters per 100 words
S = int((sentences * 100.0) / words)  # average number of sentences per 100 words
X = round(0.0588 * L - 0.296 * S - 15.8)


if X < 1:
    print("Before Grade 1")
elif X > 16:
    print("Grade 16")
else:
    print(f"Grade {X}")
