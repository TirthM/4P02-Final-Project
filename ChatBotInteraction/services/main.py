# COSC 4P02 - Brock University Chat Bot

import random  # choosing random response respectively
import numpy as np  # numpy
import nltk  # Natural Language Tool Kil
import json  # feeding and reading data
import pickle  # pickle

from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer

words = pickle.load(open('services/words.pkl', 'rb'))
classes = pickle.load(open('services/classes.pkl', 'rb'))
training_model = load_model('services/chatbot_model.model.h5')

intents = json.loads(open('services/brock_data_set.json').read())
lemma = WordNetLemmatizer()


def words_bag(sentence):
    words_as_sentence = nltk.word_tokenize(sentence)
    words_as_sentence = [lemma.lemmatize(word) for word in words_as_sentence]
    bag_of_words = len(words) * [0]

    for w in words_as_sentence:
        for i, word in enumerate(words):
            if word == w:
                bag_of_words[i] = 1
    return np.array(bag_of_words)


def obtain_response(intents_list, intents_json):
    list_of_intents = intents_json['intents']
    topic = intents_list[0]['intent']
    option = random

    for i in list_of_intents:
        if i['topic'] == topic:
            result = option.choice(i['responses'])
    return result


def predict_message(sentence):
    error_rate = 0.25
    return_response_list = []
    bag_of_words = words_bag(sentence)
    resp = training_model.predict(np.array([bag_of_words]))[0]

    result = [[x, y] for x, y in enumerate(resp) if y > error_rate]
    result.sort(reverse=True, key=lambda a: a[1])

    for r in result:
        return_response_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_response_list


#print("The Brock Chat Bot is now Running, Start your conversation: ")

#while True:
#    message = input("")
#    msg = predict_message(message)
#    res = obtain_response(msg, intents)
#    print(res)
