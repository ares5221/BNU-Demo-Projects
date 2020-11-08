import numpy as np
import re

import sys
from six.moves import cPickle as pickle
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf

# string to be classified
str_input = "this is truly a masterful movie!"


# Clean the text, with the option to remove stopwords
def clean_text(text, remove_stopwords=True):
    print("Cleaning input..")

    text = text.lower()  # make it all in lower case

    # Optionally, remove stop words
    if remove_stopwords:
        stopwords = np.loadtxt("dataset/stopwords.txt", dtype='str')

    # Clean the text
    text = re.sub(r"<br />", " ", text)
    text = re.sub(r"[^a-z]", " ", text)
    text = re.sub(r"   ", " ", text)  # Remove any extra spaces
    text = re.sub(r"  ", " ", text)

    if remove_stopwords:
        word_list = text.split();
        text = ' '.join([i for i in word_list if i not in stopwords])

    print("Finished cleaning dataset")
    return text


all_data = pickle.load(open('dataset.pickle', 'rb'))
tokenizer = all_data['tokenizer']  # load tokenizer of dataset
max_review_length = all_data['max_review_length']  # load pad length used in pre processing
del all_data

# clean text
str_input = clean_text(str_input)

# tokinizing input
print("Tokenizing input..")
input_seq = tokenizer.texts_to_sequences([str_input])
print("Tokenizing is complete.")

# padding input
print("Padding input..")
input_pad = pad_sequences(input_seq, maxlen=max_review_length)
print("Padding is complete")

# load best model if found
try:
    print("Loading model...")

    best_accuracy_on_test_file = pickle.load(open('./best_model/best_model_info.pickle', 'rb'))
    best_accuracy_folder_name = best_accuracy_on_test_file['folder_name']
    del best_accuracy_on_test_file
    folder_path = "./best_model/{}/".format(best_accuracy_folder_name)
    model_saver = tf.train.import_meta_graph("{}model.ckpt.meta".format(folder_path))
    print("Model loaded")

except:
    print("Please run train script first and make sure best_model folder contains a checkpoint to load")
    sys.exit()


def classifyReview(input):
    print("restoring checkpoint and classifying...")
    with tf.Session() as sess:
        model_saver.restore(sess, tf.train.latest_checkpoint(folder_path))  # restore latest checkpoint
        graph = sess.graph
        inputs = graph.get_tensor_by_name("inputs/inputs:0")  # get input tensor
        batch_size = graph.get_tensor_by_name("inputs/batch_size:0")  # get batch_size tensor

        fully_connected_keep_prob = graph.get_tensor_by_name(
            "inputs/fully_connected_keep_prob:0")  # get fully_connected_keep_prob tensor
        lstm_output_keep_prob = graph.get_tensor_by_name(
            "inputs/lstm_output_keep_prob:0")  # get lstm_output_keep_prob tensor

        predictions = graph.get_tensor_by_name("predictions/predictions:0")  # get predictions tensor
        # making input in correct format
        np_input = np.zeros((1, max_review_length), dtype=int)
        np_input[0] = input
        # set feed dictionary
        feed_dict = {inputs: np_input, lstm_output_keep_prob: 1, fully_connected_keep_prob: 1, batch_size: 1}
        # get predictions by feedforward

        predictions = sess.run(
            [predictions], feed_dict=feed_dict)
        return predictions[0]
    print("classified")


answer = classifyReview(input_pad)

print("Predicted '{}' as: ".format(str_input));

if answer >= 0.5:
    print("Good movie")
else:
    print("Bad movie")
