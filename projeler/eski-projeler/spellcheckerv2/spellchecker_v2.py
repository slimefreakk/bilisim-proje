from difflib import get_close_matches


def wordlist(wordlistfile: str):
    with open(wordlistfile) as file:
        wordlist = []
        for word in file:
            wordlist.append(word.strip())
    return wordlist

word_list = wordlist("wordlist.txt")
text = input("Write text: ")
words = text.split(" ")
checked_sentence = ""
wrong_words = []
for word in words:
    if word.lower() in word_list:
        checked_sentence += (word + " ")
    else:
        checked_sentence += (f"*{word}* ")
        wrong_words.append(word)
print(checked_sentence.strip())


if len(wrong_words) != 0:
    print("suggestions:")
    for wrong_word in wrong_words:
        close_mathces = get_close_matches(wrong_word, word_list)
        print(wrong_word + ": " + ", ".join(close_mathces))
