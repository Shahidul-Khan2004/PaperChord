from nltk import word_tokenize, sent_tokenize

text = input("Enter the text: ")

print(sent_tokenize(text))
print(word_tokenize(text))