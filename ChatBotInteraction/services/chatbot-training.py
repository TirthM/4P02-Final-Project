#COSC 4P02 - Brock University Chat Bot

import random
import numpy as np
import nltk
import json
import pickle

from tensorflow.keras.layers import Activation, Dropout, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from nltk.stem import WordNetLemmatizer

intents_data = json.loads(open('brock_data_set.json').read())
lemma = WordNetLemmatizer()

classes = []
docs = []
word_letters = []
training_list = []                                               #This list will be used to initialize the training data. used in fill_training_list method.
chars_to_ignore = ['!', ',', '.', '?']                           #Letters to ignore from the data file. Non-useful characters that do not provide any input.

# this method uses the training list and initializes training data.
# Uses tokenized words from the docs list and lemmatizes each word
# a lemmatized word is used to represent the likeness of certain words
# the bag of words list is used to append any lemmatized words that = the related pattern
# the output row list consists of '0' for a tag and '1' for current tag
def fill_training_list(training_list, docs, classes, word_letters):
    output_null = len(classes) * [0]

    for doc in docs:
        bag_of_words = []
        word_patterns = doc[0]
        word_patterns = [lemma.lemmatize(word.lower()) for word in word_patterns]
        for word in word_letters:
            bag_of_words.append(1) if word in word_patterns else bag_of_words.append(0)

        output_row = list(output_null)
        output_row[classes.index(doc[1])] = 1
        training_list.append([bag_of_words, output_row])

# this method takes each word from the borck_data_set file and tokenizes it
# the for loop splits a larger body of text into smaller lines through the process of tokenization
# adds the tokenized word into a list called docs corelating th word to its respective topic - [(['tokenized word'],'topic')]
# adds the topics/classes in a list called classes ['topic'] - example topic - About
def tokenize(classes, docs, word_letters):
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)
            word_letters.extend(word_list)
            docs.append((word_list, intent['topic']))
            if intent['topic'] not in classes:
                classes.append(intent['topic'])

# this method creates the model which is used as training parameters for the dataset.
# the model consists of 3 layers - (first hidden layer) 128 neurons, dropout rate of 0.5 between each layer
# (second hidden layer) 64 neurons, the last hidden layer consists the amount of neuros = to the number of intents
# the last layer will be used to calculate/predict the outcome (response) using softmax
# the purpose of this model is to confirm accuracy of returning the correct response
def create_model(train_coord_x, train_coord_y):
    model = Sequential()
    a = train_coord_x
    b = train_coord_y

    model.add(Dense(128, input_shape=(len(a[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(b[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    training_result = model.fit(np.array(train_coord_x), np.array(train_coord_y), batch_size=5, verbose=1 , epochs=200)
    model.save('chatbot_model.model.h5', training_result)
    print("training model is complete!")

# this method prints the lists that have been used to log tokenized words
# used to confirm if the words are correctly organized.
def print_list(classes, docs, word_letters):
    print("LAYOUT OF EACH LIST: ")

    print("Documents List: ")
    print(len(docs))
    print(docs)

    print("Letters & Words List: ")
    print(len(word_letters))
    print(word_letters)

    print("Classes List: ")
    print(len(classes))
    print(classes)

# this method dumps the classes and word_letters list into a pickle file converting the content into a bytestream.
# Pickle is used to store all the tag names to classify when we are predicting the response/output.
def pickle_dump(classes, word_letters):
    pickle.dump(classes, open('classes.pkl', 'wb'))
    pickle.dump(word_letters, open('words.pkl', 'wb'))

#Script Begins

tokenize(classes, docs, word_letters)

word_letters = [lemma.lemmatize(word) for word in word_letters if word not in chars_to_ignore]
word_letters = sorted(set(word_letters))
classes = sorted(set(classes))

pickle_dump(classes, word_letters)
fill_training_list(training_list, docs, classes, word_letters)

random.shuffle(training_list)
training_list = np.array(training_list)
train_coord_x = list(training_list[:, 0])
train_coord_y = list(training_list[:, 1])

create_model(train_coord_x, train_coord_y)
print_list(classes, docs, word_letters)



