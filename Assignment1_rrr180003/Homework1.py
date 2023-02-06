import pathlib
import pickle
import re
import sys
import nltk
from nltk import word_tokenize
import csv


class Person:
#initialize person class
    def __init__(self, last, first, middleinitial, ID, officephone):
        self.last = last
        self.first = first
        self.middleinitial = middleinitial
        self.ID = ID
        self.officephone = officephone
    
    def display(self):
    #display method
        print(f"Employee ID: {self.ID} \t {self.first} {self.middleinitial} {self.last} \t {self.officephone}")

def preprocess():
#preprocess methods
        people = []
        with open('C:\develop\workspace_python\Assignment1_rrr180003\data\data.csv', 'r') as f:
            csvreader = csv.reader(f)
            next(csvreader)
            fieldnames = ['Last','First','Middle Initial','ID','Office phone']
            reader = csv.DictReader(f, fieldnames=fieldnames)

            #read through csv and separate values
            for row in reader:
                first = row['First']
                first.capitalize()
                last = row['Last']
                last.capitalize()
                middle = row['Middle Initial']
                if(middle == ''):
                    middle = 'X'
                else:
                    middle.capitalize()
                id = row['ID']
                id_pattern = "^[A-Za-z]{2}[0-9]{4}$"
                if not re.match(id_pattern, id):
                    id.upper()
                officephone = row['Office phone']   
                phone_pattern = "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
                if not re.match(phone_pattern, officephone):
                    officephone = re.sub('[^0-9]', '', officephone)
                #add person class objects and add to a dictionary with key
                person = Person(first,last,middle,id,officephone)
                people.append(person)
                person.display()
        return people

#sys arg arguments to check file path
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()
    
    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

people = {}
people = preprocess()

#pickle file processing
with open('persons', 'wb') as file:
    pickle.dump(people, file)
    file.close()

with open('persons', 'rb') as file:
    persons = pickle.load(file)
    file.close()

for id, person in persons.items():
    print(f'Employee id: {person.id}')
    print(f'\t {person.first_name}, {person.middle_initial}, {person.last_name}, {person.phone}')





            
