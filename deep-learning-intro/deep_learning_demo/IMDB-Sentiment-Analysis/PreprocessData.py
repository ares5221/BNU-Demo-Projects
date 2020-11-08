# Dataset link: https://www.kaggle.com/c/word2vec-nlp-tutorial/data

import pandas as pd
import numpy as np
import re

from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from six.moves import cPickle as pickle

# read labeled training set
print("Loading dataset..")
train = pd.read_csv("dataset/labeledTrainData.tsv", delimiter="\t")
print("Finished loading dataset")


# Clean the text, with the option to remove stopwords
def clean_text(text, remove_stopwords=True):
    print("Cleaning dataset..")

    size = text.shape[0]
    reviews = np.empty(size, dtype=object)
    labels = np.zeros(size, dtype=int)

    index = 0
    for list in text:
        name = list[0]
        label = list[1]
        review = list[2].lower()  # make it lower case
        reviews[index] = review
        labels[index] = label
        index = index + 1

    # load stopwords
    if remove_stopwords:
        stopwords = np.loadtxt("dataset/stopwords.txt", dtype='str')

    for i in range(size):

        # Clean the text
        reviews[i] = re.sub(r"<br />", " ", reviews[i])
        reviews[i] = re.sub(r"[^a-z]", " ", reviews[i])
        reviews[i] = re.sub(r"   ", " ", reviews[i])  # Remove any extra spaces
        reviews[i] = re.sub(r"  ", " ", reviews[i])

        # remove stop words
        if remove_stopwords:
            word_list = reviews[i].split();
            reviews[i] = ' '.join([i for i in word_list if i not in stopwords])

    print("Finished cleaning dataset")

    # Return a list of words & labels
    return reviews, labels


train_clean, train_labels = clean_text(train.values, True)
print(train_clean[0])
# Tokenize the reviews
print("Tokenizing dataset..")
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_clean)  # give each word a unique id
print("Tokenizing is complete.")
print(train_clean[0])
word_index = tokenizer.word_index  # final id
# print("word index: " + str(word_index))

train_seq = tokenizer.texts_to_sequences(train_clean)  # convert dataset to ids
print("train_seq is complete.")
print(train_seq[0])
# Pad the reviews

max_review_length = 200

print("Padding dataset..")
train_pad = pad_sequences(train_seq, maxlen=max_review_length)  # padded with max length
review_lengths_longer_than_pad = 0
for seq in train_seq:  # calculate how many reviews longer than pad length
    if len(seq) > max_review_length:
        review_lengths_longer_than_pad = review_lengths_longer_than_pad + 1

print("Number of reviews longer than pad length({}): {}".format(max_review_length, review_lengths_longer_than_pad))

print("train_pad is complete.")
print(train_pad[0])
# Split the reviews into training, validation, and testing
print("Splitting dataset..")
x_train, x_test, y_train, y_test = train_test_split(train_pad, train_labels, test_size=0.20, random_state=2)
x_test, x_valid, y_test, y_valid = train_test_split(x_test, y_test, test_size=0.20, random_state=2)
print("Done splitting data")

# save data to a pickle file to load when training
print("Saving data into pickle file")

pickle_file = 'dataset.pickle'

try:
    f = open(pickle_file, 'wb')
    save = {
        'train_dataset': x_train,
        'train_labels': y_train,
        'test_dataset': x_test,
        'test_labels': y_test,
        'valid_dataset': x_valid,
        'valid_labels': y_valid,
        'num_of_words': len(word_index),
        'tokenizer': tokenizer,
        'max_review_length': max_review_length
    }
    pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
    f.close()
    print("Done")
except Exception as e:
    print('Unable to save data to', pickle_file, ':', e)
    raise
