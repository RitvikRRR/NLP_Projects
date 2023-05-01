import openai
import spacy
import csv
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
from nltk.stem import WordNetLemmatizer


openai.api_key = "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"

messages = [
    {"role": "system", "content": "You are SweetBot, a dessert recipe chatbot. "
                                  "You will give the user recipes and instructions for making various desserts. "
                                  "Keep your responses brief. "},
]


def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        print("SweetBot: " + reply)


def NER_comparison(all_txt):
    nlp = spacy.load('en_core_web_sm')
    NER = {}
    doc = nlp(all_txt)
    for ent in doc.ents:
        NER[ent.text] = ent.label_
    return NER


def nltk_POS(raw_text):
    # Uses a list comprehension to remove non alphas and make lower case
    tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
    # Remove stop words and words with length 5 or less
    removedStops = [t for t in tokens if t not in stopwords and len(t) > 2]
    # Lemmatizing tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in removedStops]
    uniqueLemmas = set(lemmatized)
    # POS Tagging, uses regex to find POS that start with N to filter for nouns
    tags = nltk.pos_tag(uniqueLemmas)
    # print(tags)
    nounLemmas = [token for token, pos in tags if re.match(r'^N', pos)]

    return nounLemmas


if __name__ == '__main__':
    print('SweetBot: Hi there! I am SweetBot, a dessert recipe chatbot. What is your name?')
    name_input = input()
    ner = NER_comparison(name_input)

    name = ''
    name_check = False
    while name_check is False:
        for text, label in ner.items():
            if label == 'PERSON':
                name_check = True
                name = text
                break
        if name_check is False:
            print('SweetBot: Sorry, I could not recognize a name. Please try to input it again.')
            name_input = input()
            ner = NER_comparison(name_input)
    # print(ner)

    user_db = {}
    with open('user_model.csv', mode='r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            names = row['Name']
            allergies = row['Allergies']
            user_db[names] = allergies
    # print(user_db)

    if name in user_db:
        if user_db[name] != '':
            print('SweetBot: It\'s good to see you again, ' + name + '! You are allergic to ' + user_db[name] + '.')
        else:
            print('SweetBot: It\'s good to see you again, ' + name + '! You have no food allergies')

        while True:
            print('SweetBot: What dessert would you like a recipe for?')
            dessert = input()
            if dessert.lower() == 'quit':
                break

            if user_db[name] != '':
                chatbot(name + ' has requested a recipe for (' + dessert + '). If possible, find a recipe that excludes'
                                                                           ' the following food items: ' + user_db[
                            name])
            else:
                chatbot(name + ' has requested a recipe for (' + dessert + ').')

    else:
        print('SweetBot: Hi there ' + name + "! Please list any foods you are allergic to or say \'None\'.")
        allergies_input = input()
        allergies_text = ''
        if allergies_input.lower() == 'none':
            pass
        else:
            nouns = nltk_POS(allergies_input)
            # print(nouns)
            for text in nouns:
                allergies_text += text + ', '

        with open('user_model.csv', mode='a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csvfile.write('\n')
            csv_writer.writerow([name, allergies_text])

        while True:
            print('SweetBot: What dessert would you like a recipe for?')
            dessert = input()
            if dessert.lower() == 'quit':
                break

            if allergies_text != '':
                chatbot(
                    name + ' has requested a recipe for (' + dessert + '). If possible, find a recipe that excludes '
                                                                       'the following food items: ' + allergies_text)
            else:
                chatbot(name + ' has requested a recipe for (' + dessert + ').')
