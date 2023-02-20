import nltk
import sys
import pathlib
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from random import seed
from random import randint

#guessing game function
def guessinggame():
    #random generation of the word decided from the list of 50 most occuring words.
    random = randint(0,49)
    select_word = most_common[random][0]

    print("Let's play a word guessing game!\n")

    cur_score = 5
    gameOver = False

    while gameOver == True:
        for i in range(len(select_word)):
            print("_")
        guess = input("Guess a letter: ")

        if guess == '!':
            print("Game has ended!")
            exit
        elif guess not in select_word:
            cur_score = cur_score - 1
            print(f"Sorry, guess again. Score is {cur_score}")
        elif guess in select_word:
            cur_score = cur_score + 1
            print(f"Right! Score is {cur_score}")
            
#opens and reads file
f = open('anat19.txt','r') 
text = f.read()
f.close()

#tokenizes text to read
tokens = word_tokenize(text)
tokens_low = [t.lower() for t in tokens]
prep_tokens = [t for t in tokens_low if t.isalpha() and t not in stopwords.words('english')]

#lemmatizes the text and separates into unique lemmas
wnl = WordNetLemmatizer()
lemmas = [wnl.lemmatize(t) for t in prep_tokens]
unique_lemmas = list(set(lemmas))

#separates tokens into their respective pos
tags = pos_tag(unique_lemmas)
first_tags = tags[:20]

#turns text into textblob object in order to use it for processing and separate it into nouns
blob = TextBlob(text)
noun_list = blob.noun_phrases

#creates a dictionary of the 50 most commonly seen tokens found within the text file
counts = {t:lemmas.count(t) for t in unique_lemmas}
sorted_counts = sorted(counts.items(), key = lambda x : x[1], reverse = True)
most_common = []
for i in range(50):
    most_common.append(sorted_counts[i])



# sys arg arguments to check file path
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()
    
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

guessinggame()