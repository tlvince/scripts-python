WORDS = {
    "altruism",
    "orthodoxy",
    "extol",
    "pervade"
}

def rotate(word, i):
    print(word)
    word = word[1:] + word[0]
    i = i - 1
    if i != 0:
        rotate(word, i)

def main():
    for word in WORDS:
        rotate(word, len(word))

if __name__ == '__main__':
    main()
